# Used by the application (Flask and core_queries.py). 
import mysql.connector
def get_connection():
    """Establish MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anshu22@31@123",  # your password
            database="oil_supply_chain"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None
