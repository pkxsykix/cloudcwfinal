from flask import Flask, request, jsonify
import time
import http.client
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Stock Analysis API!"

@app.route('/warmup', methods=['POST'])
def warmup():
    req_data = request.get_json()

    # Check if 's' and 'r' are provided in the request
    s = req_data.get('s')
    r = req_data.get('r')
    if s is None or r is None:
        return jsonify({"error": "'s' and 'r' parameters are required."}), 400

    if s == 'lambda':
        # Call app.py for Lambda warm-up
        subprocess.run(["python", "app.py"])
        return jsonify({"result": "Lambda warm-up initiated."})

    elif s == 'ec2':
        # Call app_ec2.py for EC2 warm-up
        subprocess.run(["python", "app_ec2.py"])
        return jsonify({"result": "EC2 warm-up initiated."})

    else:
        return jsonify({"error": "Invalid value for 's'. Must be 'lambda' or 'ec2'."}), 400

if __name__ == "__main__":
    app.run(debug=True)
