import time
from flask import Flask, request, jsonify, render_template
import requests
import numpy as np
import yfinance as yf
import random
import matplotlib.pyplot as plt
from flask_cors import CORS
import boto3
import sys
from flask import Flask, request, jsonify
import time
import boto3

app = Flask(__name__)

@app.route('/analyse', methods=['POST'])
def analyse():
    # Make a request to the EC2 instance to perform Monte Carlo simulation
    response = requests.post(f"{EC2_URL}/monte_carlo", json=request.json)

    # Return the response from EC2
    return jsonify(response.json())

@app.route('/', methods=['POST'])
def create_instance():
    # EC2 instance creation logic
    user_data = """#!/bin/bash
            apt update -y
            apt install python3 apache2 -y
            apache2ctl restart
            wget https://gitlab.surrey.ac.uk/vn00197/comm034/-/raw/main/aws_ec2.py -P /var/www/html
            chmod 755 /var/www/html/aws_ec2.py
            wget https://gitlab.surrey.ac.uk/vn00197/comm034/-/raw/main/apache2.conf -O /etc/apache2/apache2.conf
            a2enmod cgi
            service apache2 restart"""
    st = time.time()
    ec2 = boto3.resource('ec2', region_name='your-region')  # Replace 'your-region' with your region
    instances = ec2.create_instances(
        ImageId='your-ami-id',  # Replace 'your-ami-id' with your AMI ID
        MinCount=1,  # Minimum number of instances to create
        MaxCount=1,  # Maximum number of instances to create
        InstanceType='t2.micro',
        KeyName='your-key-name',  # Replace 'your-key-name' with your key pair name
        SecurityGroups=['SSH'],  # Replace 'SSH' with your security group
        UserData=user_data
    )
    dnss = []
    for i in instances:
        i.wait_until_running()
        i.load()
        dnss.append(i.public_dns_name)
    time.sleep(60)
    return jsonify({'note': f"Currently running {len(dnss)} EC2 instances"})

if __name__ == "__main__":
    app.run(debug=True)
