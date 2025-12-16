import mysql.connector
import pandas as pd

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='anshu22@31@123',  # your password
            database='oil_supply_chain'
        )
        if connection.is_connected():
            print("✅ Connected to database.")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

def insert_refineries():
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()
    print("📄 Reading Excel file...")
    df = pd.read_excel(r'C:\Users\anshu\OneDrive\Desktop\dbms project\backend\Refineries.xlsx')

    print("✅ Excel file loaded. Columns:")
    print(df.columns)
    print("🔍 First few rows:")
    print(df.head())

    print("💾 Inserting data into database...")

    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO refineries (refinery_id, refinery_name, location, capacity, processed_today, efficiency)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['refinery_id'],
                row['refinery_name'],
                row['location'],
                row['capacity'],
                row['processed_today'],
                row['efficiency']
            ))

        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    connection.commit()
    print("✅ Data inserted successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    insert_refineries()
