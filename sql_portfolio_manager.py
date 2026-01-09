import sqlite3
import pandas as pd

# CONFIGURATION
db_name = "investment_portfolio.db"

# 1. CONNECT TO DATABASE
# This creates the file if it doesn't exist
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
print(f"Connected to database: {db_name}")

# 2. CREATE TABLE (DDL - Data Definition Language)
# We create a table to store trading execution logs
create_table_query = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL, -- 'BUY' or 'SELL'
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
);
"""
cursor.execute(create_table_query)
print("Table 'trades' created successfully.")

# 3. INSERT MOCK DATA (DML - Data Manipulation Language)
# Clearing old data to avoid duplicates if you run this script multiple times
cursor.execute("DELETE FROM trades")

# Simulating a list of trades
trades_data = [
    ('2023-01-10', 'AAPL', 'BUY', 10, 150.00),
    ('2023-01-12', 'MSFT', 'BUY', 5, 250.00),
    ('2023-02-05', 'AAPL', 'BUY', 5, 155.00),  # Buying more Apple
    ('2023-02-10', 'TSLA', 'BUY', 20, 180.00),
    ('2023-03-01', 'AAPL', 'SELL', 3, 170.00), # Taking profit on Apple
    ('2023-03-15', 'MSFT', 'BUY', 10, 260.00)
]

insert_query = "INSERT INTO trades (date, ticker, side, quantity, price) VALUES (?, ?, ?, ?, ?)"
cursor.executemany(insert_query, trades_data)
conn.commit() # Save changes
print(f"Inserted {len(trades_data)} sample trades.")

# 4. DATA ANALYSIS WITH SQL
# The goal: Calculate total holdings and average buy price per asset.
# We use SQL Aggregation (GROUP BY) instead of Python loops.

analysis_query = """
SELECT 
    ticker,
    SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END) as total_shares,
    ROUND(AVG(price), 2) as avg_execution_price,
    COUNT(*) as trade_count
FROM trades
GROUP BY ticker
HAVING total_shares > 0
ORDER BY total_shares DESC;
"""

print("\n--- SQL QUERY RESULT: PORTFOLIO SUMMARY ---")

# We use Pandas to execute the SQL and display it nicely
df_result = pd.read_sql_query(analysis_query, conn)
print(df_result)

# 5. CLOSE CONNECTION
conn.close()