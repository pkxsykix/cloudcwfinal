from flask import Flask, request, jsonify, render_template
import boto3
import numpy as np
import yfinance as yf
import random
import matplotlib.pyplot as plt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dictionary to store analysis results accessible to multiple endpoints
analysis_results = {}

# Initialize AWS SNS client
sns_client = boto3.client('sns', region_name='us-east-1')
sns_topic_arn = 'arn:aws:sns:us-east-1:123456789012:your-topic-name'

@app.route('/')
def index():
    return "Welcome to the Stock Analysis API!"

@app.route('/get_endpoints', methods=['GET'])
def get_endpoints():
    endpoints = []
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and not rule.rule.endswith('static'):
            call_string = f"curl -X GET http://{request.host}{rule.rule}"
            endpoints.append({rule.endpoint: call_string})
        elif 'POST' in rule.methods:
            call_string = f"curl -d '{{<args>}}' http://{request.host}{rule.rule}"
            endpoints.append({rule.endpoint: call_string})
    return jsonify(endpoints)

@app.route('/analyse', methods=['POST'])
def analyse():
    req_data = request.get_json()
    ticker = req_data.get('ticker', 'AMZN')
    data = yf.download(ticker, period="1y").to_json()

    # SNS payload preparation
    sns_payload = {
        "data": data,
        "parameters": req_data
    }

    # Publishing a message to SNS topic
    sns_response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps({'default': json.dumps(sns_payload)}),
        MessageStructure='json'
    )

    return jsonify({"result": "ok", "sns_response": str(sns_response)})

# Additional routes as needed...

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)  # Ensure Flask listens on all public IPs
