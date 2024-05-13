from flask import Flask, request, jsonify
import yfinance as yf
import monte_carlo

app = Flask(__name__)

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

    # Perform the Monte Carlo simulation
    results = monte_carlo.monte_carlo_simulation(h, d)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)