import mysql.connector
import pandas as pd
# 💡 BEST PRACTICE FIX: Import centralized connection
from db_config import get_connection as connect_db

def insert_shipments():
    # 💡 NOTE: The redundant connect_to_database function has been removed.
    conn = connect_db()
    if conn is None:
        print("❌ Database connection failed.")
        return

    try:
        cursor = conn.cursor()
        print("✅ Connected to database.")

        # ⚠️ FIX 1: Change file name to the correct Shipments file you created
        excel_path = r"C:\Users\anshu\OneDrive\Desktop\dbms project\backend\Shipments.xlsx" 
        print(f"📄 Reading Excel file: {excel_path}...")
        df = pd.read_excel(excel_path)
        print("✅ Excel file loaded.")

        # ⚠️ FIX 2: Use the correct SQL query and column names for the Shipments table
        query = """
        INSERT INTO Shipments (source_well_id, destination_refinery_id, quantity, transport_date, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        print("💾 Inserting data into database...")

        for _, row in df.iterrows():
            try:
                cursor.execute(query, (
                    row['source_well_id'],  # Column from the new Shipments.xlsx
                    row['destination_refinery_id'], # Column from the new Shipments.xlsx
                    row['quantity'],
                    row['transport_date'],
                    row['status']
                ))
            except Exception as e:
                print(f"⚠️ Error inserting row: {e}")

        conn.commit()
        print("✅ Data inserted successfully into Shipments.")

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔗 Connection closed.")

if __name__ == "__main__":
    insert_shipments()