
# text-sql-llm-app
A full-stack application that allows users to input natural language queries and retrieves AR invoice data from a  Snowflake database using OpenAI. The application should be built with a React frontend and a Python backend, deployed on  AWS. 
=======
React Frontend - text-sql-llm full stack Application

**Overview**

This repository contains the frontend code for the text-sql-llm full stack Application. 
The application provides features such as:
  Invoice Search: Allows users to search invoices with advanced input validation and error handling.
  Data Visualization: Displays pie charts and line charts to summarize invoice statuses and trends.
  Dynamic Table: Presents search results in a structured, responsive table.

**Setup Instructions**

To set up and run the frontend application locally, follow these steps:

**Prerequisites**
Node.js and npm: Ensure you have Node.js (v14 or later) and npm installed. You can download them from Node.js.
Build Folder: Obtain the build folder containing the precompiled assets.

**Steps to Run the Application**

  Clone the Repository:
  git clone https://github.com/pshukla81/text-sql-llm-app.git
  cd text-sql-llm-app/frontend

  Add the Build Folder:
  Copy the build folder into the frontend directory. The final structure should look like this:
  
  frontend/
  ├── build/
  ├── public/
  ├── src/
  ├── package.json
  └── README.md

  Start the Development Server:
  npm start
  The application will be available at http://localhost:3000.

  Run the Production Build If you want to serve the production build:
  npm install -g serve
  serve -s build

**Frontend Functionality**

  **Invoice Search:**
  Allows users to search invoices using a query input field.
  Validates input for SQL injection, invalid characters, and minimal query length.
  Displays error messages for invalid inputs.
  
  **Dynamic Table:**
  Presents search results in a structured, scrollable table.
  Includes columns like Subsidiary, Business Unit, Invoice Number, and more.
  
 ** Data Visualization:**
  
 ** Pie Chart:**
   Displays the breakdown of invoice statuses (Open, Paid, Overdue).
  
  **Line Charts:**
  
    Shows trends for Paid and Overdue invoices. Displays the trend of Overdue invoices over time.

  **Code Structure**

  **App.js: **
    The main component containing the application logic, including:
    State management using useState.
    Input validation logic.
    API request handling for fetching invoice data.
    Chart and table rendering.
  
  **App.css:**
    The styling file providing:
    Responsive designs for tables and charts.
    Custom tooltips and input error handling styles.





>>>>>>> eaa23e6f7b4f5886b0b1ea04aab4ea00af8f8966
