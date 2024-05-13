import json
import random

def simple_percentile(sorted_data, percentile):
    """Calculate the given percentile of a sorted list of values."""
    k = (len(sorted_data)-1) * (percentile/100.0)
    f = int(k)
    c = f + 1 if f < k else f
    if c < len(sorted_data):
        return sorted_data[f] + (sorted_data[c] - sorted_data[f]) * (k - f)
    return sorted_data[f]

def lambda_handler(event, context):
    # Use .get() to safely access 'data' with default to empty dict if not provided
    data = event.get('data', {})  # Now defaults to {} if 'data' is not provided
    params = event.get('parameters', {})

    h = params.get('h', 101)
    d = params.get('d', 10000)
    t = params.get('t', 'sell')  # Not used in the simulation
    p = params.get('p', 7)  # Not used in the simulation

    # Perform the Monte Carlo simulation
    results = {"VaR 95": [], "VaR 99": [], "Profit/Loss": []}
    for _ in range(d):
        simulated = [random.gauss(0.05, 0.1) for _ in range(h)]
        simulated.sort()
        results["var95"].append(simple_percentile(simulated, 5))
        results["var99"].append(simple_percentile(simulated, 1))
        results["Profit/Loss"].append(random.uniform(-100, 100))

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }