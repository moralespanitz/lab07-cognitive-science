import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rates', methods=['GET'])
def get_exchange_rates():
    """Fetch exchange rates for USD, EUR, and SOL"""
    try:
        # Using exchangerate-api.com free tier
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        rates = {
            "USD": data["rates"].get("USD", 1.0),
            "EUR": data["rates"].get("EUR", 0),
            "PEN": data["rates"].get("PEN", 0),  # Peruvian Sol
            "timestamp": data.get("time_last_updated")
        }
        return jsonify(rates), 200
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
        if 'rates' in raw_path:
            # Fetch exchange rates
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            rates = {
                "USD": data["rates"].get("USD", 1.0),
                "EUR": data["rates"].get("EUR", 0),
                "PEN": data["rates"].get("PEN", 0),
                "timestamp": data.get("time_last_updated")
            }

            return {
                'statusCode': 200,
                'body': json.dumps(rates),
                'headers': {'Content-Type': 'application/json'}
            }
        elif 'health' in raw_path:
            return {
                'statusCode': 200,
                'body': json.dumps({"status": "healthy"}),
                'headers': {'Content-Type': 'application/json'}
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Exchange Rate API - use /rates or /health"}),
                'headers': {'Content-Type': 'application/json'}
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

if __name__ == '__main__':
    app.run(debug=True)
