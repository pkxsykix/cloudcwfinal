from flask import Flask, request, jsonify
import boto3
import yfinance as yf
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Initialize AWS EC2 and SNS clients
ec2 = boto3.resource('ec2')
sns_client = boto3.client('sns', region_name='us-east-1')
sns_topic_arn = 'arn:aws:sns:us-east-1:123456789012:your-topic-name'

def create_ec2_instance():
    user_data_script = """#!/bin/bash
    sudo yum update -y
    sudo yum install git -y
    git clone https://github.com/yourusername/yourrepository.git /path/to/clone
    cd /path/to/clone
    sudo pip install -r requirements.txt
    python your_script.py
    """
    instance = ec2.create_instances(
        ImageId='ami-xxxxxxx',  # Replace with your actual AMI ID
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='YourKeyName',  # Replace with your actual key name
        UserData=user_data_script,
        SecurityGroupIds=['sg-xxxxxxxx'],  # Replace with your actual security group ID
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'API_Server'}
                ]
            }
        ]
    )
    return instance[0].id

# Automatically create an EC2 instance on app startup
instance_id = create_ec2_instance()
print(f"EC2 instance {instance_id} created and setup initiated.")

@app.route('/')
def index():
    return "Welcome to the Stock Analysis API!"

@app.route('/analyse', methods=['POST'])
def analyse():
    req_data = request.get_json()
    ticker = req_data.get('ticker', 'AMZN')
    data = yf.download(ticker, period="1y").to_json()

    # Prepare payload for SNS to trigger the Lambda function
    sns_payload = {
        "data": data,
        "parameters": req_data
    }

    # Publish a message to SNS topic
    sns_response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(sns_payload)
    )

    return jsonify({"result": "ok", "sns_response": str(sns_response)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
