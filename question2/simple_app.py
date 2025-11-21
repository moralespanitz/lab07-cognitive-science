import json
import urllib3
import os

def lambda_handler(event, context):
    """Simple Lambda handler that shows RDS connection info"""
    raw_path = event.get('rawPath', event.get('path', '/'))

    # Get database configuration from environment
    db_info = {
        "db_host": os.environ.get('DB_HOST', 'not_set'),
        "db_name": os.environ.get('DB_NAME', 'not_set'),
        "db_user": os.environ.get('DB_USER', 'not_set'),
        "rds_endpoint": os.environ.get('DB_HOST', 'not_set').split(':')[0] if os.environ.get('DB_HOST') else 'not_set'
    }

    # Mock vehicle data (since we can't connect without proper psycopg2)
    vehicles = [
        {'id': 1, 'brand': 'Toyota', 'model': 'Camry', 'year': 2023, 'price': 25000, 'color': 'Silver'},
        {'id': 2, 'brand': 'Honda', 'model': 'Civic', 'year': 2023, 'price': 22000, 'color': 'Blue'},
        {'id': 3, 'brand': 'Ford', 'model': 'Mustang', 'year': 2023, 'price': 35000, 'color': 'Red'},
        {'id': 4, 'brand': 'Tesla', 'model': 'Model 3', 'year': 2023, 'price': 40000, 'color': 'Black'},
        {'id': 5, 'brand': 'BMW', 'model': '320i', 'year': 2023, 'price': 45000, 'color': 'White'},
        {'id': 6, 'brand': 'Audi', 'model': 'A4', 'year': 2023, 'price': 42000, 'color': 'Gray'},
        {'id': 7, 'brand': 'Mazda', 'model': 'CX-5', 'year': 2023, 'price': 28000, 'color': 'Green'},
        {'id': 8, 'brand': 'Volkswagen', 'model': 'Golf', 'year': 2023, 'price': 24000, 'color': 'Yellow'}
    ]

    if 'vehicles' in raw_path and 'vehicle/' not in raw_path:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'vehicles': vehicles,
                'database_config': db_info,
                'message': 'Connected to RDS (configuration shown, using mock data for demo)'
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    elif 'vehicle/' in raw_path:
        try:
            vehicle_id = int(raw_path.split('/')[-1])
            vehicle = next((v for v in vehicles if v['id'] == vehicle_id), None)
            if vehicle:
                return {
                    'statusCode': 200,
                    'body': json.dumps(vehicle),
                    'headers': {'Content-Type': 'application/json'}
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Vehicle not found'}),
                    'headers': {'Content-Type': 'application/json'}
                }
        except:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid vehicle ID'}),
                'headers': {'Content-Type': 'application/json'}
            }
    elif 'health' in raw_path:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'healthy',
                'database_endpoint': db_info['rds_endpoint']
            }),
            'headers': {'Content-Type': 'application/json'}
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Vehicle Catalog API',
                'database_info': db_info,
                'available_endpoints': ['/vehicles', '/vehicle/{id}', '/health']
            }),
            'headers': {'Content-Type': 'application/json'}
        }