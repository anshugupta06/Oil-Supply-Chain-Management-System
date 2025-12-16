# python library used to connect and interact with MySQL databases.
# It allows you to:Connect to a MySQL server, Run SQL queries, Fetch results, Handle database errors
# Used for testing/debugging. Its main purpose is to be run directly to confirm the 
# database server is running and the credentials are correct.

import mysql.connector
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='anshu22@31@123',  # 🔁 Replace with your actual MySQL password
            database='oil_supply_chain'
        )

        if connection.is_connected():
            print("✅ Successfully connected to the database.")
        return connection

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    connect_to_database()
