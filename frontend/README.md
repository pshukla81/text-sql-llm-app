
# React Frontend - text-sql-llm full stack Application

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

**1. Clone the Repository:**
  git clone https://github.com/pshukla81/text-sql-llm-app.git
  cd text-sql-llm-app/frontend

  The final structure should look like this:
  
  frontend/
  
  ├── public/
  ├── src/
  ├── package.json
  └── README.md

**2. Create an .env file for x-token for authentication and API end point server name.**
     
 **3. Start the Development Server:**
  npm start
  The application will be available at http://localhost:3000.

 **4. Run the Production Build If you want to serve the production build:**
  npm install -g serve
  serve -s build









