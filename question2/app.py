import json
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Mock vehicle data (simulating database)
VEHICLES_DATA = [
    {'id': 1, 'brand': 'Toyota', 'model': 'Camry', 'year': 2023, 'price': 25000, 'color': 'Silver', 'engine': '2.5L', 'fuel_type': 'Gasoline'},
    {'id': 2, 'brand': 'Honda', 'model': 'Civic', 'year': 2023, 'price': 22000, 'color': 'Blue', 'engine': '1.8L', 'fuel_type': 'Gasoline'},
    {'id': 3, 'brand': 'Ford', 'model': 'Mustang', 'year': 2023, 'price': 35000, 'color': 'Red', 'engine': '3.0L', 'fuel_type': 'Gasoline'},
    {'id': 4, 'brand': 'Tesla', 'model': 'Model 3', 'year': 2023, 'price': 40000, 'color': 'Black', 'engine': 'Electric', 'fuel_type': 'Electric'},
    {'id': 5, 'brand': 'BMW', 'model': '320i', 'year': 2023, 'price': 45000, 'color': 'White', 'engine': '2.0L', 'fuel_type': 'Gasoline'},
    {'id': 6, 'brand': 'Audi', 'model': 'A4', 'year': 2023, 'price': 42000, 'color': 'Gray', 'engine': '2.0L', 'fuel_type': 'Diesel'},
    {'id': 7, 'brand': 'Mazda', 'model': 'CX-5', 'year': 2023, 'price': 28000, 'color': 'Green', 'engine': '2.5L', 'fuel_type': 'Gasoline'},
    {'id': 8, 'brand': 'Volkswagen', 'model': 'Golf', 'year': 2023, 'price': 24000, 'color': 'Yellow', 'engine': '1.4L', 'fuel_type': 'Gasoline'}
]

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    """Get all vehicles from catalog"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, brand, model, year, price, color, engine, fuel_type FROM vehicles')
        rows = cur.fetchall()
        cur.close()
        conn.close()

        vehicles = []
        for row in rows:
            vehicles.append({
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'year': row[3],
                'price': float(row[4]),
                'color': row[5],
                'engine': row[6],
                'fuel_type': row[7]
            })

        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    """Get specific vehicle by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, brand, model, year, price, color, engine, fuel_type FROM vehicles WHERE id = %s', (vehicle_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return jsonify({"error": "Vehicle not found"}), 404

        vehicle = {
            'id': row[0],
            'brand': row[1],
            'model': row[2],
            'year': row[3],
            'price': float(row[4]),
            'color': row[5],
            'engine': row[6],
            'fuel_type': row[7]
        }
        return jsonify(vehicle), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

def lambda_handler(event, context):
    """AWS Lambda handler for Lambda URL"""
    # Lambda URL format
    raw_path = event.get('rawPath', event.get('path', '/'))

    try:
        # Initialize database on first call
        init_db()

        if 'vehicles' in raw_path and 'vehicle/' not in raw_path:
            # List all vehicles
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id, brand, model, year, price, color, engine, fuel_type FROM vehicles')
            rows = cur.fetchall()
            cur.close()
            conn.close()

            vehicles = []
            for row in rows:
                vehicles.append({
                    'id': row[0],
                    'brand': row[1],
                    'model': row[2],
                    'year': row[3],
                    'price': float(row[4]),
                    'color': row[5],
                    'engine': row[6],
                    'fuel_type': row[7]
                })

            return {
                'statusCode': 200,
                'body': json.dumps(vehicles),
                'headers': {'Content-Type': 'application/json'}
            }
        elif 'vehicle/' in raw_path:
            # Get specific vehicle
            vehicle_id = int(raw_path.split('/')[-1])
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT id, brand, model, year, price, color, engine, fuel_type FROM vehicles WHERE id = %s', (vehicle_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if not row:
                return {
                    'statusCode': 404,
                    'body': json.dumps({"error": "Vehicle not found"}),
                    'headers': {'Content-Type': 'application/json'}
                }

            vehicle = {
                'id': row[0],
                'brand': row[1],
                'model': row[2],
                'year': row[3],
                'price': float(row[4]),
                'color': row[5],
                'engine': row[6],
                'fuel_type': row[7]
            }
            return {
                'statusCode': 200,
                'body': json.dumps(vehicle),
                'headers': {'Content-Type': 'application/json'}
            }
        elif 'health' in raw_path:
            return {
                'statusCode': 200,
                'body': json.dumps({"status": "healthy", "database": "connected"}),
                'headers': {'Content-Type': 'application/json'}
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Vehicle Catalog API - use /vehicles or /vehicle/{id}"}),
                'headers': {'Content-Type': 'application/json'}
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
