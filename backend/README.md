# FastAPI Application

This repository contains the code for a simple FastAPI application located in the `repo/backend` folder. The instructions below will guide you through downloading the code, setting up the environment, installing dependencies, and running the application.

## Folder Structure

The FastAPI app is located in the `backend` folder of the repository:


## Requirements

- Python 3.x (Ensure you have Python 3.7 or higher)
- `pip` (Python's package installer)
- A virtual environment (optional but recommended)

## Setup Instructions

Follow these steps to get the application running locally.

### 1. Clone the Repository

First, clone the repository to your local machine:


git clone https://github.com/pshukla81/text-sql-llm-app.git
cd yourrepository/backend

**2. Set Up a Virtual Environment (Optional but Recommended)**
Create a virtual environment to isolate the dependencies:

On Windows:
python -m venv .venv
.\.venv\Scripts\activate

On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

****3. Install Dependencies****
Once the virtual environment is activated, install the required dependencies listed in the requirements.txt file:

pip install -r requirements.txt
This will install all the required libraries, including FastAPI and Uvicorn (for running the server).
**
4. Run the FastAPI Application**
To start the FastAPI server, run the following command:

uvicorn main:app --reload
main refers to the main.py file in the backend folder.
app refers to the FastAPI app instance in the main.py file.
The --reload flag allows for automatic code reloading during development.
After running the above command, the server should start, and you'll see output like this:

INFO:     Will watch for changes in these directories: ['.', 'backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
**5. Access the Application**
Once the server is running, you can access the FastAPI app in your browser, through an API tool like Postman or React frontend code provided in the repository

The app will be available at http://127.0.0.1:8000.

**6. Stop the Server**
To stop the server, simply press CTRL+C in the terminal where the server is running.

**Additional Notes**
Make sure to check the requirements.txt file to verify the versions of dependencies.
