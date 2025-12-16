import mysql.connector
import pandas as pd

#establish a connection between your Python program and your MySQL database.
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='anshu22@31@123',
            database='oil_supply_chain'
        )
        if connection.is_connected():
            print("✅ Connected to database.")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

# Its job is to load equipment data from an Excel file and insert it into the MySQL database.
def insert_equipments():
    connection = connect_to_database()
    if connection is None:
        return
    cursor = connection.cursor()

    # ✅ Correct file path (make sure the file name matches exactly)
    excel_path = r'C:\Users\anshu\OneDrive\Desktop\dbms project\backend\Equipment.xlsx'

    print("📄 Reading Excel file...")
    df = pd.read_excel(excel_path)
    print("✅ Excel file loaded. Columns:")
    print(df.columns.tolist())

    # ✅ Check if expected columns exist
    expected_columns = ['equipment_id', 'equipment_name', 'location', 'status', 'last_service_date', 'next_service_due']
    for col in expected_columns:
        if col not in df.columns:
            print(f"⚠️ Missing column in Excel: {col}")
            return

    # ✅ Insert data
    print("💾 Inserting data into database...")
    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO equipment (equipment_id, equipment_name, location, status, last_service_date, next_service_due)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['equipment_id'],
                row['equipment_name'],
                row['location'],
                row['status'],
                row['last_service_date'],
                row['next_service_due']
            ))
        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    connection.commit()
    print("✅ Data inserted successfully.")
    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_equipments()
