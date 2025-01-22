
import openai
from fastapi import FastAPI, HTTPException
from fastapi import Depends, Header
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import snowflake.connector
from typing import List, Any, Dict
from dotenv import load_dotenv
import os
import time
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables
load_dotenv()
# Set OpenAI API key
# Ensure OpenAI API key is present in environment variables
openai_api_key = os.getenv("OPENAI_API_KEY") 
if not openai_api_key:
    raise HTTPException(status_code=500, detail="OpenAI API key not found in environment variables")


# Snowflake connection parameters
SNOWFLAKE_USER =  os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# LLM Model Configuration (for easy modification)
LLM_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 150,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

app = FastAPI()
# Allowing local host for cross origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with specific origins or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)
# code to implement a basic rate limiter
limiter = Limiter(key_func=get_remote_address)

# Caching for schema
schema_cache = {"last_fetched": None, "data": None}

# Set up the exception handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_error(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse("Too Many Requests", status_code=429)



# Dependency to validate the token
async def verify_token(x_token: str = Header(...)):
    # print(f"{x_token}")
    if x_token != os.getenv("API_ACCESS_TOKEN"):
        raise HTTPException(status_code=401, detail="Unauthorized access")



# Input model for the endpoint
class Query(BaseModel):
    query: str

# Function to connect to Snowflake
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

# Function to get table schema with caching
def get_table_schema():
    current_time = time.time()
    if schema_cache["last_fetched"] and current_time - schema_cache["last_fetched"] < 7200:  # Cache for 5 minutes
        return schema_cache["data"]

    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DESCRIBE TABLE AR_INVOICE_DETAILS")
        columns = cursor.fetchall()
        schema_description = "Table ar_invoice_details has the following columns:\n"
        for column in columns:
            column_name, column_type, *_ = column
            schema_description += f"- {column_name} ({column_type})\n"
        schema_cache["data"] = schema_description
        schema_cache["last_fetched"] = current_time
        return schema_description
    finally:
        conn.close()

# Function to specify functional constraints and validations on the `ar_invoice_details` table
def preprocess_query() -> str:
    """
    Defines rules for parsing, preprocessing NLQ and returns them as a string.

    Returns:
        str: A string containing preprocessing rules for NLQ.
    """
    # Initialize
    preprocessing = []

    # Add default preprocessing rules
    preprocessing.append("The following parsing, cleaning, deduplication, shortening apply to NLQ:")
    preprocessing.append("- Remove unnecessary characters and whitespace")
    preprocessing.append("- Deduplicate repeated words or phrases")
    preprocessing.append("- Shorten the text if it's longer than 100 characters while retaining meaning")
    preprocessing.append("- Return the cleaned and formatted query in plain text")
    preprocessing.append("- Remove any sql queries to prevent sql injection.")
    preprocessing.append("- Remove any DDL or DML queries to prevent sql injection.")
    # Join all constraints into a single string with line breaks
    return "\n".join(preprocessing)

# Function to specify functional constraints and validations on the `ar_invoice_details` table
def get_functional_constraints() -> str:
    """
    Builds functional constraints line by line and returns them as a string.

    Returns:
        str: A string containing functional constraints for query generation.
    """
    # Initialize the constraints
    constraints = []

    # Add default functional constraints
    constraints.append("The following functional constraints apply for generating SQL queries:")
    constraints.append("- Ensure column names and table names strictly match the database schema.")
    constraints.append("- Avoid using SQL functions or syntax unsupported by Snowflake db.")
    constraints.append("- If filtering, use valid column values from the schema.")
    constraints.append("- Limit results to a reasonable number of rows (e.g., top 100 rows).")
    constraints.append("- Sort the results by relevant columns where applicable.")
    constraints.append("- Only apply filtering when query has specified that. For example List all Invoices should simply list all invoices without any invoice status check")
    constraints.append("- Pending invoices are synomyous with Invoice status of Open.")
    constraints.append("- Due,Overdue invoices are synomyous with Invoice status of Past Due.")
    constraints.append("- When filtering for specific invoices statuses dont filter for other Invoice statuses")
    constraints.append("- Calculate invoice_aging_bucket from the invoice_due_date")
    constraints.append("- Always use ILike in the where clause to perform case insensitive searches. For example given the text to list all open invoices, resulting query will be       SELECT * FROM ar_invoice_details WHERE INVOICE_STATUS ILIKE '%OPEN%'ORDER BY INVOICE_DUE_DATE LIMIT 100;")
    constraints.append("Given the text input 'List all overdue invoices', the resulting query will be SELECT * FROM ar_invoice_details WHERE INVOICE_STATUS ILIKE '%Past Due%' ORDER  BY  INVOICE_DUE_DATE LIMIT 100;")
    constraints.append("- Always prefix and suffix % to the search strings in the where clause")
    constraints.append("- Dont use INTERVAL syntax for date calculations; instead, use simple arithmetic (e.g., CURRENT_DATE + 7) and/or Snowflake specific queries DATEADD, DATEDIFF")
    constraints.append("Snowflake automatically caches query results. Reuse cached results with RESULT_SCAN. For example SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));")

    # Join all constraints into a single string with line breaks
    return "\n".join(constraints)

    

# Function to execute SQL query on Snowflake
def execute_sql_on_snowflake(sql_query: str):
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


# Text to Sql generation Endpoint
# Adds a basic rate limiter
# Adds basic token based security to the endpoint
# Performs basic validation on the input
# Constructs the prompt by passing the table schema from the db
# Enhances prompt by adding more stringent input validations and functionalconstraints on the data to generate sql with a higher accuracy

@app.post("/v1/generate_sql")
@limiter.limit("100/minute")  # Limit to 100 requests per minute
async def generate_sql(request: Request, user_query: Query, token: str = Depends(verify_token)):
    body = await request.json()
    # print(f"Request Body: {body}")
    try:
        # Validate input
        # print(f"sql input: {user_query}") # Print sql input for debugging
        if not user_query.query :
            raise HTTPException(status_code=400, detail="Invalid Input : Search must be a non-empty string")
        if not user_query.query or len(user_query.query) < 15 :
            raise HTTPException(status_code=400, detail="Invalid Input : Search text must be more descriptive.")

        # Get schema from Snowflake
        table_schema = get_table_schema()

        # Get functional_constraints
        functional_constraints = get_functional_constraints()
        preprocessing = preprocess_query()
        # Prepare the prompt
        prompt = f"""
        Preprocess natural language query, consider following database schema and functional constraints, and convert the processed query into a valid SQL query:
        
        {preprocessing}
        {table_schema}
        
        Query:
        {user_query.query}
        {functional_constraints} # constraints have to be put after the query else they get overriden
        """

        # Call OpenAI API to generate SQL query
        # print(f"Loaded OpenAI API Key: {openai_api_key}") Print key for debugging
        response = openai.chat.completions.create(
            model=LLM_CONFIG["model"],
            messages=[
                {"role": "system", "content": "You are an AI assistant that parses, preprocesses natural language query and then generates valid SQL queries based on a given schema and      functional constraints."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=LLM_CONFIG["max_tokens"],
            temperature=LLM_CONFIG["temperature"],
            top_p=LLM_CONFIG["top_p"],
            frequency_penalty=LLM_CONFIG["frequency_penalty"],
            presence_penalty=LLM_CONFIG["presence_penalty"]
        )

        # Extract and validate the SQL query
        raw_sql_query = response.choices[0].message.content.strip()
        # print(f"Generated raw sql :\n{raw_sql_query}")  # raw query result for debugging

        # Clean the SQL query using regex
        import re
        match = re.search(r"(SELECT .*?;)", raw_sql_query, re.DOTALL | re.IGNORECASE)
        
        if match:
            sql_query = match.group(1).strip()  # Extract the valid SQL query
        else:
            raise HTTPException(status_code=400, detail="Generated query is not a valid SQL SELECT statement.")

        # Execute the query on Snowflake
        query_result = execute_sql_on_snowflake(sql_query)
        
        
       	# print(f"Generated Query :\n{sql_query}")  # Log cleaned query for debugging
        # print(f"Generated data :\n{query_result}")  # Log data for debugging
       	# Format the result as a JSON object
        return {"results": query_result, "status": 200}
                  
       
    except openai.OpenAIError as e:
        raise HTTPException(status_code=503, detail=f"OpenAI service error: {str(e)}")
    except snowflake.connector.errors.ProgrammingError as e:
        raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
