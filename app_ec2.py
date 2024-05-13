import time
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


@app.route('/calculate', methods=['POST'])
def initHandler():
    if request.method == 'POST':
        global s, r
        s = request.form.get('s')
        r = request.form.get('r')

        if s == 'lambda':
            conn = http.client.HTTPSConnection("7g8hgv09ae.execute-api.us-east-1.amazonaws.com")
            return doRender('form.htm', {'note': "Connected to " + str(conn)})
        elif s == 'ec2':
            ec2 = boto3.resource('ec2', region_name='us-east-1')
            user_data = """#!/bin/bash
            apt update -y
            apt install python3 apache2 -y
            apache2ctl restart
            wget https://gitlab.surrey.ac.uk/vn00197/comm034/-/raw/main/aws_ec2.py -P /var/www/html
            chmod 755 /var/www/html/aws_ec2.py
            wget https://gitlab.surrey.ac.uk/vn00197/comm034/-/raw/main/apache2.conf -O /etc/apache2/apache2.conf
            a2enmod cgi
            service apache2 restart"""
            global st
            st = time.time()
            instances = ec2.create_instances(
                ImageId='ami-07caf09b362be10b8',
                MinCount=int(r),
                MaxCount=int(r),
                InstanceType='t2.micro',
                KeyName='kp-nvirginia.pem',
                SecurityGroups=['SSH'],
                UserData=user_data
            )
            global dnss
            dnss = []
            for i in instances:
                i.wait_until_running()
                i.load()
                dnss.append(i.public_dns_name)
            time.sleep(60)
            return doRender('form.htm', {'note': "Currently running " + str(len(dnss)) + " EC2 instances"})


@app.route('/analyse', methods=['POST'])
def analyse():
    # Process the analysis request
    req_data = request.get_json()
    h = req_data.get('h', 101)
    d = req_data.get('d', 10000)
    t = req_data.get('t', 'sell')
    p = req_data.get('p', 7)
    
    # Fetch the stock data using yfinance based on 'ticker' provided or default to 'AMZN'
    ticker = req_data.get('ticker', 'AMZN')
    data = yf.download(ticker, period="1y").to_json()
    
    # Call the /analyse endpoint locally
    local_analyse_response = analyze_data(data, h, d, t, p)

    return jsonify(local_analyse_response)

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