import mysql.connector
import pandas as pd

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='anshu22@31@123',  # your MySQL password
            database='oil_supply_chain'
        )
        if connection.is_connected():
            print("✅ Connected to database.")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

def insert_data():
    connection = connect_to_database()
    if connection is None:
        return

    cursor = connection.cursor()

    # Read Excel file
    print("📄 Reading Excel file...")
    df = pd.read_excel(r'C:\Users\anshu\OneDrive\Desktop\dbms project\backend\Wells.xlsx')

    print("✅ Excel file loaded. Columns:")
    print(df.columns)

    # Check first few rows
    print("🔍 First few rows:")
    print(df.head())

    # Insert data row by row
    print("💾 Inserting data into database...")

    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO wells (
                    well_id, well_name, location, capacity_per_day,
                    current_output, pressure_level, temperature, last_inspection_date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['well_id'],
                row['well_name'],
                row['location'],
                row['capacity_per_day'],
                row['current_output'],
                row['pressure_level'],
                row['temperature'],
                row['last_inspection_date']
            ))
        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    connection.commit()
    print("✅ Data inserted successfully.")
    cursor.close()
    connection.close()

if __name__ == "__main__":
    insert_data()
