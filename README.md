# Investment Portfolio SQL Tracker

A Python-based ETL (Extract, Transform, Load) tool designed to manage an investment trading log using a relational database. This project integrates Python with SQLite to create a persistent data storage system, simulate trading activity, and execute complex SQL queries for portfolio analysis.

## Project Overview
Unlike standard CSV-based analysis, this tool leverages a SQL engine to handle data integrity and aggregation. It demonstrates the ability to perform CRUD (Create, Read, Update, Delete) operations and bridge the gap between database management and Python data science tools.

## Key Features
* **Database Architecture:** Automatically initializes a SQLite database and defines the schema (DDL) for trading logs.
* **Data Manipulation:** Simulates transactional data insertion (DML) for buy/sell orders.
* **Advanced Reporting:** Uses SQL aggregation to transform raw trade logs into a consolidated portfolio view.
* **Pandas Integration:** Fetches SQL query results directly into a DataFrame for presentation.

## Technical Deep Dive: The SQL Logic
The core of the analysis relies on a single, optimized SQL query that calculates current holdings and average buy price. It utilizes:
* **CASE WHEN Statements:** To handle the directional logic (adding quantity for Buys, subtracting for Sells).
* **GROUP BY Clauses:** To aggregate individual trades by ticker symbol.
* **HAVING Filters:** To exclude closed positions (zero holdings) from the report.

```sql
SELECT 
    ticker,
    SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END) as total_shares,
    ROUND(AVG(price), 2) as avg_execution_price,
    COUNT(*) as trade_count
FROM trades
GROUP BY ticker
HAVING total_shares > 0
ORDER BY total_shares DESC;
