import React, { useState } from "react";
import { Line, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "./App.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const App = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [tableData, setTableData] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [hasError, setHasError] = useState(false);
  const [loading, setLoading] = useState(false);
  const [searchPressed, setSearchPressed] = useState(1);
  const forbiddenKeywords = /(?:\b(DROP|DELETE|INSERT|UPDATE|ALTER|EXEC|CREATE|REPLACE|TRUNCATE|MERGE|GRANT|REVOKE)\b)/i;

  // Sample chart data
  const pieData = {
    labels: ["Open", "Paid", "Overdue"], // Labels for the pie slices
    datasets: [
      {
        data: [5, 10, 3], // Values for each category
        backgroundColor: [
          "rgba(8, 70, 213, 0.6)", // Cool blue for "Open"
          "rgba(34, 114, 3, 0.6)", // Cool green for "Paid"
          "rgba(235, 29, 6, 0.53)", // red for "Overdue"
        ],
        borderColor: [
          "rgba(8, 70, 213, 0.9)", // Darker blue border for "Open"
          "rgba(34, 114, 3, 0.9)", // Darker green border for "Paid"
          "rgba(235, 29, 6, 0.53)" // red for "Overdue"
        ],
        borderWidth: 1, // Border width
      },
    ],
  };

  // Options to customize the look of the chart
const pieOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: "top", // Position of the legend
      labels: {
        font: {
          size: 14, // Font size for legend
        },
        color: "#333", // Legend text color
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          let label = context.label || '';
          let value = context.raw || 0;
          return `${label}: ${value}`;
        },
      },
    },
  },
};

  const doubleLineData = {
    labels: ["January", "February", "March", "April", "May", "June"], // X-axis labels
    datasets: [
      {
        label: "Paid", // Dataset label
        data: [65, 59, 80, 81, 56, 55], // Y-axis data points
        fill: false, // Don't fill the area under the line
        borderColor: "rgba(75, 192, 192, 1)", // Line color
        tension: 0.1, // Smoothing of the line
      },
      {
        label: "Overdue", // Dataset label
        data: [28, 48, 40, 19, 86, 27], // Y-axis data points for revenue
        fill: false,
        borderColor: "rgba(153, 102, 255, 1)", // Line color for revenue
        tension: 0.1,
      },
    ],
  };

  const lineData = {
    labels: ["January", "February", "March", "April", "May", "June"], // X-axis labels
    datasets: [
      {
        label: "Overdue", // Label for the dataset
        data: [65, 59, 80, 81, 56, 55], // Data points for the Y-axis (Sales data)
        fill: false, // Don't fill the area under the line
        borderColor: "rgba(235, 29, 6, 0.53)", // Line color (red)
        tension: 0.1, // Smoothing of the line
      },
    ],
  };
  

  const chartOptions = {
    scales: {
      x: {
        grid: {
          color: "rgba(0, 123, 255, 0.1)",
        },
      },
      y: {
        grid: {
          color: "rgba(0, 123, 255, 0.1)",
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: "#007bff",
        },
      },
    },
  };

  // Form submission handler
  const handleSearch = async (e) => {
    e.preventDefault();

    // Basic input validation
    if (!searchQuery.trim()) {
      setErrorMessage("Search text cannot be empty");
      setHasError(true);
      return;
    }
    // Invalid character validation
    if (/['";]/.test()) {
      setErrorMessage("Search text cannot have invalid characters.");
      setHasError(true);
      return;
    }
    // Sql Injection validation
    if (forbiddenKeywords.test(searchQuery)) {
      setErrorMessage("Search text cannot have forbidden SQL keywords.");
      setHasError(true);
      return;
    }

    if (searchQuery.length <= 15) {
      setErrorMessage("Please describe your search a little more.");
      setHasError(true);
      return;
    }

    setErrorMessage(""); // Clear errors
    setHasError(false); // Reset error state if input is valid
    setLoading(true); // Start loading
    setSearchPressed(2); //Set search pressed to a different value

    const apiToken = process.env.REACT_APP_API_ACCESS_TOKEN;
    const apiUrl = process.env.REACT_APP_API_URL;
    // console.log(apiToken); // Ensure the token is being loaded correctly
    // console.log(apiUrl); // Ensure the token is being loaded correctly
    // console.log(`${apiUrl}/v1/generate_sql)`)

    try {
      const response = await fetch(`${apiUrl}/v1/generate_sql`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-token": `${apiToken}`,
        },
        body: JSON.stringify({ query: searchQuery }),
      })
      

      if (!response.ok) {
      // console.log(response)
      throw new Error(`Server responded with status ${response}`);
      }

      const data = await response.json();
      // console.log(JSON.stringify(data))
      //console.log(data)
      
      // Ensure data structure is as expected
      if (data.results && Array.isArray(data.results)) {
        setTableData(data.results);
      }
    } catch (err) {
      console.error("Error fetching data:", err);
      setErrorMessage(
        "An error occurred while fetching data. Please try again later or contact support."
      );
    }
    finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div>
      {/* Navbar */}
      <div className="navbar">
        <div className="logo">
          <span style={{ fontSize: "30px", marginRight: "10px" }}>📊</span>
          <b>Finvibe</b>
        </div>
        <ul className="menu">
          <li className="user-icon">👤</li>
          <li>Invoices</li>
          <li>Customers</li>
          <li>Reports</li>
        </ul>
      </div>

      <div className="app-container">
        {/* Section 1: Welcome message */}
        <div className="section welcome-section">
          <div className="app-header">
            <h1>
              Welcome to the Invoices Search!{" "}
              <span role="img" aria-label="celebratory star">
                ✨
              </span>
              <span className="beta-tag">Beta</span>
            </h1>
            <div className="welcome-text">
              A brand-new way to search your invoices with ease. Let's get
              started!
            </div>
          </div>
        </div>

        {/* Section 2: Text input and search icon */}
        <div className="section search-section">
          <div className="search-container">
            <form className="search-form" onSubmit={handleSearch}>
              <div className="tooltip">
                <input
                  type="text"
                  className={`search-input ${hasError ? "input-error" : ""}`}
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Start typing and press enter to search for Invoices..."
                  style={{ width: "95%" }}
                />
              </div>
              <div className="tooltip-container">
                <button type="submit" className="search-button">
                  🔍
                </button>
                <span className="tooltip-text">Click on the search icon to submit the query</span>
              </div>
            </form>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
          </div>
        </div>

        {/* Section 3: Table section */}
        {loading ? ( // Spinner while loading
          <div className="spinner">Loading...</div>
        ) : (
          !errorMessage && tableData && tableData.length > 0 ? (
            <div className="section table-section">
              <p>{tableData.length} rows returned</p>
              <table className="table-container">
                <thead className="table-header">
                  <tr>
                    <th>Subsidiary</th>
                    <th>Business Unit</th>
                    <th>Customer Name</th>
                    <th>Invoice Number</th>
                    <th>Invoice Date</th>
                    <th>Invoice Status</th>
                    <th>Invoice Due Date</th>
                    <th>Invoice Aging Bucket</th>
                    <th>Memo</th>
                    <th>Invoice Original Amount (Local)</th>
                    <th>Invoice Original Amount (USD)</th>
                    <th>Invoice Open Amount (Local)</th>
                    <th>Invoice Open Amount (USD)</th>
                    <th>Invoice Due Amount (Local)</th>
                    <th>Invoice Due Amount (USD)</th>
                  </tr>
                </thead>
                <tbody className="table-body">
                  {tableData.map((row, index) => (
                    <tr className="table-row" key={index}>
                      {Object.values(row).map((value, idx) => (
                        <td className="table-data" key={idx}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            !errorMessage && searchQuery && (searchPressed !=1 || (searchPressed ==2 && !tableData)) && <p className="spinner">
              No results found for this search text. Please try again with a different text.
            </p>
          )
        )}


        {/* Section 4: Charts section */}
        <div className="section charts-section">
          <div className="chart-container">
            <h3>Invoices Breakdown</h3>
            <Pie data={pieData} options={chartOptions} />
          </div>
          <div className="chart-container">
            <h3>Invoices Status Trend</h3>
            <Line data={doubleLineData} options={chartOptions} />
          </div>
          <div className="chart-container">
            <h3>Overdue Invoices Trend</h3>
            <Line data={lineData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
