import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='anshu22@31@123',
            database='oil_supply_chain'
        )
        if conn.is_connected():
            print("✅ Connected to database.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

def check_table_counts(conn):
    cursor = conn.cursor()      #Creates a cursor object, which allows Python to execute SQL commands.
    tables = [
        "Wells",
        "Shipments",
        "Refineries",
        "Retail_Outlets",
        "Equipment",
        "Maintenance_Logs"
    ]

    print("\n📊 Record counts in each table:\n")
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")     #counts how many rows (records) are present in that table.
            count = cursor.fetchone()[0]        # Fetches the count result 
            print(f"🟩 {table}: {count} records")
        except mysql.connector.Error as err:
            print(f"⚠️ Error checking {table}: {err}")

    cursor.close()


def main():
    conn = connect_to_database()
    if conn:
        check_table_counts(conn)
        conn.close()
        print("\n🔒 MySQL connection closed.")


if __name__ == "__main__":
    main()
