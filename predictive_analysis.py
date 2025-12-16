import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import numpy as np
import json

# ------------------ DATABASE CONNECTION (Your original function) ------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anshu22@31@123", 
            database="oil_supply_chain"
        )
        return connection
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None


# ------------------ WELL PRODUCTION FORECAST (UPDATED) ------------------
def predict_well_output():
    conn = connect_db()
    if conn is None:
        return {"error": "Database connection failed"}

    # ⚠️ FIX: Added well_name to the query for chart labels
    query = """
        SELECT well_id, well_name, capacity_per_day, current_output, pressure_level, temperature
        FROM Wells
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return {"error": "No data found in Wells table"}

    # Simple regression model: predict future output based on pressure & temperature
    X = df[["pressure_level", "temperature"]]
    y = df["current_output"]

    model = LinearRegression()
    model.fit(X, y)

    future_prediction = model.predict(X)

    df["predicted_output"] = np.round(future_prediction, 2)

    return json.loads(df.to_json(orient="records"))


# ------------------ EQUIPMENT HEALTH ANOMALY DETECTION (UPDATED) ------------------
def detect_equipment_anomalies():
    conn = connect_db()
    if conn is None:
        return {"error": "Database connection failed"}

    #Added equipment_name to the query for chart labels
    query = """
        SELECT equipment_id, equipment_name, DATEDIFF(CURDATE(), last_service_date) AS days_since_service
        FROM Equipment
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        return {"error": "No data found in Equipment table"}

    # Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.1, random_state=42) #means 10% of the data is assumed to be anomalies and sets a seed value to make results consistent every time you run the code
    df["anomaly_score"] = model.fit_predict(df[["days_since_service"]])

    # Original logic for status mapping retained
    df["status"] = df["anomaly_score"].apply(lambda x: "⚠️ Needs Attention" if x == -1 else "✅ Normal")

    return json.loads(df.to_json(orient="records"))


# ------------------ TESTING LOCALLY ------------------
if __name__ == "__main__":
    print("🔮 Predicting Well Output...")
    print(json.dumps(predict_well_output(), indent=4))

    print("\n🛠 Detecting Equipment Anomalies...")
    print(json.dumps(detect_equipment_anomalies(), indent=4))