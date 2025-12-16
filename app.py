from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS 
from db_config import get_connection
from core_queries import fetch_core_metrics, optimize_shipment_routes 
from ml_models.predictive_analysis import predict_well_output, detect_equipment_anomalies
import os
import mysql.connector # Added for better error handling in routes

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# -------------------- CRITICAL FIX: ENABLE CORS --------------------
# This allows the JavaScript running in your browser to fetch data
# from the Flask API running on localhost:5000
CORS(app) 
# -------------------------------------------------------------------

# -------------------- HOME ROUTE --------------------
@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')


# -------------------- CORE METRICS --------------------
@app.route("/api/core_metrics", methods=["GET"])
def get_core_metrics():
    data = fetch_core_metrics()
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch metrics"}), 500

# -------------------- LOGISTICS OPTIMIZATION (UPDATED) --------------------
@app.route('/api/analytics/logistics_optimization', methods=['GET'])
def api_logistics_optimization():
    try:
        # ✅ FIX: Removed company_id=1 argument, as core_queries.py
        # function does not accept it. The function now uses the 
        # stock_status column set by your database trigger.
        result = optimize_shipment_routes() 
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------- WELLS --------------------
@app.route('/api/wells')
def get_wells():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Wells;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- REFINERIES --------------------
@app.route('/api/refineries')
def get_refineries():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Refineries;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- SHIPMENTS --------------------
@app.route('/api/shipments')
def get_shipments():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Shipments;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- RETAIL OUTLETS --------------------
@app.route('/api/retail_outlets')
def get_outlets():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Retail_Outlets;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- EQUIPMENT --------------------
@app.route('/api/equipment')
def get_equipment():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Equipment;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- MAINTENANCE LOGS --------------------
@app.route('/api/maintenance_logs')
def get_maintenance_logs():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Maintenance_Logs;")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- ANALYTICS QUERIES --------------------
@app.route('/api/analytics/well_output')
def well_output():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT well_name, SUM(current_output) AS total_output
            FROM Wells
            GROUP BY well_name;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


@app.route('/api/analytics/refinery_performance')
def refinery_performance():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT refinery_name, capacity, processed_today,
                   ROUND((processed_today / capacity) * 100, 2) AS efficiency_percent
            FROM Refineries;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        # Data returns a column named 'efficiency_percent'
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


@app.route('/api/analytics/retail_sales')
def retail_sales():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT refinery_id,
                   SUM(daily_sales) AS total_sales,
                   SUM(stock_level) AS total_stock
            FROM Retail_Outlets
            GROUP BY refinery_id;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


@app.route('/api/analytics/equipment_status')
def equipment_status():
    conn = get_connection()
    if conn is None: return jsonify({"error": "DB connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT status, COUNT(*) AS count
            FROM Equipment
            GROUP BY status;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database query failed: {str(e)}"}), 500
    finally:
        if conn.is_connected(): conn.close()


# -------------------- PREDICTIVE ANALYSIS (ML) --------------------
@app.route('/api/predict_well_output', methods=['GET'])
def api_predict_well_output():
    try:
        result = predict_well_output()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/predict_equipment_anomalies', methods=['GET'])
def api_equipment_anomalies():
    try:
        result = detect_equipment_anomalies()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# -------------------- MAIN --------------------
if __name__ == '__main__':
    # Running Flask with debug=True is good for development
    app.run(debug=True)
