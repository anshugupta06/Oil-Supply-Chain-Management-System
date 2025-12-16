import mysql.connector
from mysql.connector import Error
import pandas as pd # Required for data processing and logistics optimization
import json # converting results into a frontend-friendly format.

# ------------------ DATABASE CONNECTION HELPER ------------------
# Encapsulating connection logic based on your provided code
def _get_manual_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anshu22@31@123", # ✅ your MySQL password
            database="oil_supply_chain"
        )
        return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None

# ------------------ CORE METRICS (For Dashboard Overview) ------------------
# This function retrieves all the key data insights your dashboard might display.
def fetch_core_metrics():
    connection = _get_manual_connection()
    if connection is None:
        return {"error": "Failed to connect to database"}
    
    try:
        if connection.is_connected():
            print("✅ Connected to database.")
            cursor = connection.cursor(dictionary=True)
            metrics = {}

            # 1️⃣ Total Oil Extracted per Well
            cursor.execute("""
                SELECT well_name, current_output AS current_production, capacity_per_day
                FROM Wells
                ORDER BY current_output DESC;
            """)
            metrics['well_production'] = cursor.fetchall()

            # 2️⃣ Refinery Efficiency Overview (CRITICAL FIX APPLIED HERE)
            refinery_query = """
                SELECT 
                    refinery_name, 
                    capacity, 
                    processed_today, 
                    efficiency 
                FROM Refineries
                ORDER BY efficiency DESC;
            """
            cursor.execute(refinery_query)
            refinery_rows = cursor.fetchall()

            processed_refinery_data = []
            for row in refinery_rows:
                # Explicitly convert the efficiency value to a float to prevent JS chart errors.
                try:
                    efficiency = float(row.get('efficiency'))
                except (TypeError, ValueError):
                    efficiency = 0.0 # Safety fallback
                
                processed_refinery_data.append({
                    'refinery_name': row.get('refinery_name'),
                    'total_output': row.get('processed_today'),
                    'total_capacity': row.get('capacity'),
                    # Ensure key name matches frontend expectation
                    'efficiency_percent': round(efficiency, 2)
                })
            metrics['refinery_performance'] = processed_refinery_data

            # 3️⃣ Shipments Summary
            cursor.execute("""
                SELECT COUNT(*) AS total_shipments
                FROM Shipments;
            """)
            metrics['shipment_status'] = cursor.fetchall()

            # 4️⃣ Retail Outlet Sales Summary : Now includes refinery_name for the new chart
            cursor.execute("""
                SELECT R.refinery_name, SUM(O.daily_sales) AS total_sales, SUM(O.stock_level) AS total_stock
                FROM Retail_Outlets O
                JOIN Refineries R ON O.refinery_id = R.refinery_id
                GROUP BY R.refinery_name;
            """)
            metrics['retail_sales'] = cursor.fetchall()

            # 5️⃣ Equipment Health Overview
            cursor.execute("""
                SELECT equipment_name, location, next_service_due
                FROM Equipment
                ORDER BY next_service_due ASC;
            """)
            metrics['equipment_status'] = cursor.fetchall()

            return metrics

    except Error as e:
        print("❌ Database Error Occurred!")
        print(f"Error details: {e}")
        return {"error": f"MySQL error: {str(e)}"}

    except Exception as ex:
        print("⚠️ Unexpected Error!")
        print(f"Error details: {ex}")
        return {"error": f"Unexpected error: {str(ex)}"}

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("🔒 MySQL connection closed.")

# ------------------ LOGISTICS OPTIMIZATION (UPDATED FUNCTION) ------------------
#This function uses data analytics to identify which retail outlets are most at risk of running out of stock soon.
def optimize_shipment_routes():
    """
    Identifies the retail outlets with the lowest days of stock remaining 
    to prioritize shipments, using the database's stock_status trigger logic.
    """
    conn = _get_manual_connection()
    if conn is None:
        return {"error": "Database connection failed"}
    
    # Query: Selects stock_status and orders results to show CRITICAL alerts first.
    query = """
        SELECT 
            O.outlet_name, 
            R.refinery_name, 
            O.stock_level, 
            O.daily_sales,
            (O.stock_level / O.daily_sales) AS days_of_stock_remaining,
            O.stock_status -- ✅ NEW: Select the status set by the BEFORE UPDATE trigger
        FROM Retail_Outlets O
        JOIN Refineries R ON O.refinery_id = R.refinery_id
        WHERE O.daily_sales > 0
        ORDER BY
            CASE O.stock_status -- ✅ NEW: Sort by status first, prioritizing CRITICAL
                WHEN 'CRITICAL' THEN 1
                ELSE 2
            END ASC,
            days_of_stock_remaining ASC
        LIMIT 10; -- Top 10 most critical outlets
    """
    
    try:
        # Use pandas to execute the query and process the data
        df = pd.read_sql(query, conn)
    except Exception as e:
        if conn and conn.is_connected():
            conn.close()
        return {"error": f"SQL/Pandas Error: {str(e)}"}
        
    if conn and conn.is_connected():
        conn.close()

    if df.empty:
        return {"message": "No retail data found to optimize."}

    # Format the recommendation
    df['days_of_stock_remaining'] = df['days_of_stock_remaining'].round(2)
    
    # Convert to JSON format for Flask
    recommendations = json.loads(df.to_json(orient="records"))
    
    return {
        "optimization_type": "Stock Prioritization",
        "recommendations": recommendations,
        "message": "Top 10 retail outlets requiring immediate resupply."
    }

# The template function below is now DEPRECATED. The logic was moved into fetch_core_metrics.
def get_refinery_performance():
    """DEPRECATED: Logic moved to fetch_core_metrics for unified API endpoint."""
    return []
