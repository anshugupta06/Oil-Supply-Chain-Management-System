The Oil Supply Chain Management and Predictive Analytics System is an intelligent, data-driven platform designed to optimize operations across the oil supply chain — from extraction at wells to delivery at retail outlets.
The project integrates database management, machine learning, and automation to provide a complete analytical and operational solution for real-time decision-making.
The system is built on a Flask-based Python backend connected to a MySQL database, where all operational data — including well production, refinery processing, shipments, equipment status, and retail outlet sales — is centrally stored and managed.

Key modules of the system include:

1) Wells Management – Tracks daily production, pressure, and temperature metrics to evaluate performance.

2) Refinery Operations – Monitors processing capacity, daily throughput, and efficiency rates.

3) Shipments – Maintains records of oil transportation between wells and refineries.

4) Retail Outlets – Tracks daily sales and stock levels to forecast supply requirements.

5) Equipment Maintenance – Logs service schedules and anomalies for preventive maintenance.

To enhance decision-making, the project integrates Machine Learning models:

A Linear Regression model predicts future well outputs based on parameters like pressure and temperature.


🏗️ System Architecture

The Oil Supply Chain Management and Predictive Analytics System follows a three-tier architecture, integrating the Database Layer, Backend (Application Layer), and Machine Learning & Analytics Layer for seamless data flow and intelligent automation.

🔹 Database Layer (MySQL)

Acts as the foundation of the system, storing all operational data for wells, refineries, shipments, retail outlets, equipment, and maintenance logs.

Implements SQL triggers to automatically calculate logistics health and update stock statuses in real-time.

Ensures data integrity through foreign key relationships and normalization.

🔹 Backend / Application Layer (Flask - Python)

The Flask framework serves as the middle layer, connecting the frontend or analytics dashboards with the MySQL database.

It exposes RESTful API endpoints to retrieve, insert, and analyze data.

Modules like core_queries.py and predictive_analysis.py handle data queries, aggregation, and invoke machine learning models.

Implements Flask-CORS to enable communication with future frontend dashboards.

🔹 Machine Learning & Analytics Layer

Integrates scikit-learn models for data-driven insights.

Linear Regression forecasts future oil well output based on factors like pressure and temperature.

Isolation Forest detects anomalies in equipment maintenance cycles.

Generates predictive metrics and anomaly detection outputs that are delivered through Flask APIs.

🔹 Automation Layer (SQL Trigger System)

A MySQL AFTER UPDATE trigger recalculates days_of_stock_remaining whenever a retail outlet’s sales or stock data changes.

The result is stored in the LogisticsStatus table with dynamic status labels (HEALTHY or CRITICAL), enabling automated logistics monitoring.

🔹 Frontend / Visualization (Future Integration)

Designed for compatibility with HTML, CSS, and JavaScript dashboards.

Can visualize API data such as well production trends, refinery efficiency, and equipment status in real time.

An Isolation Forest model detects anomalies in equipment service cycles, identifying machines needing urgent attention.

Additionally, a MySQL Trigger automates logistics monitoring by calculating the days of stock remaining for each retail outlet and assigning a dynamic HEALTHY or CRITICAL status.
This enables proactive resupply and ensures continuous product availability in critical distribution areas.

Through the combination of predictive analytics, real-time database automation, and RESTful API integration, the project provides a comprehensive framework for optimizing production efficiency, minimizing downtime, and improving overall supply chain reliability.

🎯 Project Objectives

1) To design and implement an intelligent oil supply chain management system
that integrates data from multiple entities — wells, refineries, shipments, retail outlets, and equipment — into a unified and efficient platform.

2) To automate real-time monitoring and analytics of production, refining, distribution, and sales activities using a centralized MySQL database and Flask-based backend.

3) To apply predictive analytics and machine learning techniques
for forecasting well production output (using Linear Regression) and detecting equipment anomalies (using Isolation Forest) to ensure preventive maintenance.

4) To enhance decision-making and logistics optimization
through intelligent data-driven insights that identify critical retail outlets requiring immediate resupply, minimizing shortages and overstocking.

5) To implement database-level automation using SQL triggers
that dynamically calculate and update logistics health status (HEALTHY / CRITICAL) based on current stock levels and daily sales data.

6) To ensure data consistency, accuracy, and scalability
by structuring the system with proper normalization, foreign key constraints, and efficient query optimization.

7) To provide an extensible backend API architecture
that can later be integrated with a dashboard or visualization layer for real-time monitoring and predictive insights.

🧠 Technology Stack
💻 1. Programming Languages

Python – for backend development, data processing, and machine learning.

SQL (MySQL) – for database management, triggers, and relational data operations.

⚙️ 2. Backend Framework

Flask (Python) – lightweight web framework used to build RESTful APIs for interacting with the database and ML models.

🗄️ 3. Database & Data Storage

MySQL – used for storing and managing all project entities (Wells, Refineries, Shipments, Retail Outlets, Equipment, Maintenance Logs).

SQL Triggers – automate logistics status updates (HEALTHY/CRITICAL) based on stock and sales data.

📊 4. Data Science & Machine Learning Libraries

Pandas – data cleaning and manipulation.

NumPy – numerical computation and array operations.

Scikit-learn –

Linear Regression for production forecasting.

Isolation Forest for anomaly detection in equipment performance.

🔐 5. Connectivity & Configuration

mysql-connector-python – connects Python scripts and Flask backend to the MySQL database.

dotenv / os (optional) – for secure configuration of database credentials.

🌐 6. Frontend (Optional / Future Integration)

HTML, CSS, JavaScript (planned) – to visualize dashboards for wells, refineries, and predictive analytics using REST API responses.

CORS (Flask-CORS) – enables cross-origin requests between frontend and backend.

🧰 7. Tools & Platforms

MySQL Workbench – for database design, queries, and trigger creation.

Visual Studio Code – for coding and managing the project structure.

Excel – used as data sources for initial dataset uploads (Wells.xlsx, Refineries.xlsx, etc.).

Postman / Browser – for testing REST API endpoints.

🏁 Project Outcome

The Oil Supply Chain Management and Predictive Analytics System successfully integrates database management, machine learning, and automation to streamline the entire oil supply process. The system efficiently stores and manages real-time data related to wells, refineries, shipments, equipment, and retail outlets using a structured MySQL database. Through the implementation of Flask-based APIs, users can easily access, analyze, and monitor key operational metrics. The machine learning models accurately predict well production output and detect equipment anomalies, enabling proactive maintenance and reducing downtime. Additionally, the SQL trigger automates logistics monitoring by dynamically calculating stock health statuses, ensuring timely resupply decisions. Overall, the project delivers a smart, data-driven solution that enhances efficiency, supports predictive decision-making, and improves the reliability and sustainability of the oil supply chain.

🚀 Project Delivery Progress

The Oil Supply Chain Management and Predictive Analytics System has been successfully developed and tested across all core modules. The database design was completed with normalized tables, foreign key relationships, and functional SQL triggers for automated stock status updates. The Flask backend was fully implemented, providing RESTful APIs to connect the database with analytics and prediction modules. All data insertion scripts were executed successfully, ensuring accurate population of the database from Excel sources. The machine learning models for well output prediction (Linear Regression) and equipment anomaly detection (Isolation Forest) were trained, validated, and integrated into the backend for real-time insights. End-to-end testing confirmed seamless interaction between the database, backend, and ML components. Overall, the project has been fully delivered, meeting all planned objectives—real-time data management, predictive analytics, and logistics automation.

⚠️ Challenges Faced

1) Database Integration Complexity – Designing and linking multiple relational tables (Wells, Refineries, Shipments, Equipment, Retail Outlets) while maintaining referential integrity required careful planning and normalization.

2) Trigger Configuration Errors – Ensuring the SQL trigger executed correctly without datatype mismatches or table reference issues was challenging, especially when automating stock status updates.

3) Machine Learning Model Selection – Choosing appropriate algorithms (Linear Regression and Isolation Forest) and tuning them to work effectively on small datasets required multiple iterations and testing.

4) Data Inconsistencies in Excel Imports – Handling missing values, incorrect data types, and formatting differences during Excel-to-MySQL insertion needed additional data validation steps.

5) Backend and Database Synchronization – Maintaining smooth communication between the Flask API and MySQL, including handling connection errors and query failures, was technically demanding.

6) Security and Configuration Management – Managing sensitive database credentials securely while keeping the system functional across different environments posed implementation challenges.

7) Scalability Considerations – Designing the system to handle future data growth and integration with visualization dashboards required careful architectural decisions.

GRAPH DESCRIPTION

<img width="1010" height="518" alt="image" src="https://github.com/user-attachments/assets/72294c08-40a7-4824-8d05-f5006fe1eb7a" />
📊 1. Logistics Optimization: Low Stock Alerts (Left Graph)
What this graph shows:

This graph identifies retail outlets that are at risk of running out of stock soon.

How it works:

The orange bars show Days of Stock Remaining, calculated as:
stock_level / daily_sales

Outlets with very low days remaining are in the critical zone and need urgent resupply.

This graph is directly powered by:
✔ SQL Trigger (after_retail_outlet_update)
✔ LogisticsStatus table
✔ Stock-level calculations in backend

Purpose:

To help logistics teams quickly recognize which outlets need immediate replenishment, preventing product shortages.

🛒 2. Retail Sales & Stock Summary (Right Graph)
What this graph shows:

This graph compares daily sales vs. current stock levels for each retail outlet.

How it works:

Green bars = Total Daily Sales

Purple bars = Total Current Stock

The comparison shows whether supply matches demand at each outlet.

Insights you get from this graph:

Outlets with high sales but low stock need priority resupply.

Outlets with excess stock but low sales indicate inefficiency or overstocking.

Helps understand sales performance and supply distribution patterns.

Purpose:

To assist retail managers in making data-driven decisions on stocking, demand forecasting, and inventory balancing.

<img width="1451" height="640" alt="image" src="https://github.com/user-attachments/assets/fed123d6-621f-4f9c-bfd7-0a103675efc7" />

🗺️ Transportation Overview (Map Visualization)
What this graph shows:

This map visualizes the real-time transportation route between a refinery and a retail outlet (or between wells → refineries depending on your data).

Elements on the Map:

🔴 Red Marker

Represents the origin point

Usually a refinery or oil well

Shows where the shipment is coming from

🔵 Blue Marker

Represents the destination point

Usually a retail outlet

Shows where the shipment is being delivered

🔺 Dashed Red Line

Represents the transportation route

Draws a path from the origin to the destination

Based on latitude and longitude stored in your database

Purpose of the Map:

To provide a geographical visualization of active shipment routes

To show where resources are supplied from and where they are delivered

Helps logistics managers identify:
✔ Distance between supply points
✔ Travel routes
✔ Potential delays or bottlenecks
✔ Geographical distribution of operations

Why this is important:

Oil supply chains depend heavily on transportation efficiency.
This map helps in:

Visual route tracking

Delivery planning

Optimizing travel time

Understanding the spatial flow of oil supply
