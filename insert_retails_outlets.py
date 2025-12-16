import mysql.connector
import pandas as pd

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


def insert_retail_outlets():
    connection = connect_to_database()
    if connection is None:
        return
    cursor = connection.cursor()

    # Read Excel file
    df = pd.read_excel(r'C:\Users\anshu\OneDrive\Desktop\dbms project\backend\_Shipments.xlsx')
    print("✅ Excel file loaded. Columns:")
    print(df.columns)

    print("💾 Inserting data into database...")
    for _, row in df.iterrows():
        try:
            query = """
                INSERT INTO retail_outlets (outlet_id, outlet_name, location, refinery_id, daily_sales, stock_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                row['outlet_id'], row['outlet_name'], row['location'],
                row['refinery_id'], row['daily_sales'], row['stock_level']
            ))
        except Exception as e:
            print(f"⚠️ Error inserting row: {e}")

    connection.commit()
    print("✅ Data inserted successfully.")
    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_retail_outlets()
