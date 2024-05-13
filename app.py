from flask import Flask, request, jsonify, render_template
import requests
import numpy as np
import yfinance as yf
import random
import matplotlib.pyplot as plt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dictionary to store analysis results accessible to multiple endpoints
analysis_results = {}

@app.route('/')
def index():
    return "Welcome to the Stock Analysis API!"

@app.route('/get_endpoints', methods=['GET'])
def get_endpoints():
    endpoints = []
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and not rule.rule.endswith('static'):  # Exclude static files
            call_string = f"curl -X GET http://{request.host}{rule.rule}"
            endpoints.append({rule.endpoint: call_string})
        elif 'POST' in rule.methods:
            # Correct the f-string by escaping braces
            call_string = f"curl -d '{{<args>}}' http://{request.host}{rule.rule}"
            endpoints.append({rule.endpoint: call_string})
    return jsonify(endpoints)


@app.route('/analyse', methods=['POST'])
def analyse():
    # Retrieve the JSON data from the request
    req_data = request.get_json()

    h = req_data.get('h', 101)  # Number of historical days for data
    d = req_data.get('d', 10000)  # Number of Monte Carlo simulations
    t = req_data.get('t', 'sell')  # Transaction type, 'sell' or 'buy'
    p = req_data.get('p', 7)  # Profit/Loss time horizon in days

    # Fetch the stock data using yfinance based on 'ticker' provided or default to 'AMZN'
    ticker = req_data.get('ticker', 'AMZN')
    data = yf.download(ticker, period="1y").to_json()

    # AWS Lambda function URL
    lambda_url = "https://646httcdkxshq6vvssr4d4a6qa0bubch.lambda-url.us-east-1.on.aws/cloudcwfinal"

    # Prepare the payload for the Lambda function
    lambda_payload = {
        "data": data,
        "parameters": {
            "h": h,
            "d": d,
            "t": t,
            "p": p
        }
    }

    lambda_response = requests.post(lambda_url, json=lambda_payload)

    # Check if the Lambda function processed the request successfully
    if lambda_response.status_code == 200:
        return jsonify({"result": "ok"})
    else:
        return jsonify({"result": "error", "message": "Failed to process data in Lambda"}), 500

@app.route('/get_sig_vars9599', methods=['GET'])
def get_sig_vars9599():
    # This could fetch data from a database or any other source
    results = {
        "var95": [random.uniform(0, 0.1) for _ in range(20)],
        "var99": [random.uniform(0, 0.1) for _ in range(20)]
    }
    return jsonify(results)

@app.route('/get_avg_vars9599', methods=['GET'])
def get_avg_vars9599():
    # Mocking average calculations
    avg_var95 = sum([random.uniform(0, 0.1) for _ in range(100)]) / 100
    avg_var99 = sum([random.uniform(0, 0.1) for _ in range(100)]) / 100
    return jsonify({'avg_var95': avg_var95, 'avg_var99': avg_var99})

@app.route('/get_sig_profit_loss', methods=['GET'])
def get_sig_profit_loss():
    # Mocking profit/loss data retrieval
    profit_loss = [random.uniform(-100, 100) for _ in range(20)]
    return jsonify({'profit_loss': profit_loss})

@app.route('/get_tot_profit_loss', methods=['GET'])
def get_tot_profit_loss():
    # Summing up the mocked profit/loss
    total_profit_loss = sum([random.uniform(-100, 100) for _ in range(100)])
    return jsonify({'total_profit_loss': total_profit_loss})

@app.route('/get_time_cost', methods=['GET'])
def get_time_cost():
    # Mocking time and cost data
    time = random.uniform(0, 100)
    cost = time * 0.05  # Assume cost is 5% of time for processing
    return jsonify({'time': time, 'cost': cost})

@app.route('/get_audit', methods=['GET'])
def get_audit():
    # Mocking audit information
    audits = [{'time': random.uniform(0, 100), 'cost': random.uniform(0, 10)} for _ in range(5)]
    return jsonify(audits)

if __name__ == "__main__":
    app.run(debug=True)