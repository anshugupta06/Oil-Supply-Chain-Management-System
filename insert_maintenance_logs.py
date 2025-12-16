import mysql.connector
import pandas as pd

def connect_to_database():
    """Connect to MySQL database"""
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


def insert_maintenance_logs():
    """Insert maintenance log data from Excel into MySQL"""
    connection = connect_to_database()
    if connection is None:
        return
    cursor = connection.cursor()

    # ✅ Excel file path
    excel_path = r'C:\Users\anshu\OneDrive\Desktop\dbms project\backend\Maintenance_Logs.xlsx'

    print("📄 Reading Excel file...")
    df = pd.read_excel(excel_path)
    print("✅ Excel file loaded. Columns found:")
    print(df.columns.tolist())

    # ✅ Insert data into table (column names same as Excel)
    print("💾 Inserting data into database...")
    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO maintenance_logs (
                    maintenance_id, equipment_id, service_date,
                    issue_reported, action_taken, technician_name
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['maintenance_id'],
                row['equipment_id'],
                row['service_date'],
                row['issue_reported'],
                row['action_taken'],
                row['technician_name']
            ))
        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    connection.commit()
    print("✅ Data inserted successfully into maintenance_logs.")
    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_maintenance_logs()
