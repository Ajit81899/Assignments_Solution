from flask import Flask, jsonify, Response
from flask_cors import CORS
import requests
import csv
from io import StringIO

app = Flask(__name__)
CORS(app)

@app.route('/get_users', methods=['GET'])
def get_users():
    response = requests.get('https://jsonplaceholder.typicode.com/users')

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data", "status_code": response.status_code})

@app.route('/generate_csv', methods=['GET'])
def generate_csv():
    response = requests.get('https://jsonplaceholder.typicode.com/users')

    if response.status_code == 200:
        data = response.json()

        # Create a CSV response
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(data[0].keys())  # Write column headers
        for item in data:
            csv_writer.writerow(item.values())  # Write data rows

        response = Response(
            csv_data.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=users.csv'}
        )

        return response
    else:
        return jsonify({"error": "Failed to retrieve data", "status_code": response.status_code})

if __name__ == '__main__':
    app.run(debug=True)
