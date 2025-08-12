from flask import Flask, jsonify
import requests

app = Flask(__name__)

#Services to be monitored
@app.route("/service1")
def service1():
    return jsonify({"message": "Service 1 is healthy"}), 200

@app.route("/service2")
def service2():
    return jsonify({"message": "Service 2 is healthy"}), 200

@app.route("/service3")
def service3():
    # Simulating a failure for the monitoring
    return jsonify({"error": "Service 3 is down"}), 500


# List of endpoints to monitor(locally run services)
SERVICES = [
    "http://127.0.0.1:5000/service1",
    "http://127.0.0.1:5000/service2",
    "http://127.0.0.1:5000/service3"
]

#  Health Check
def check_services():
    results = {}
    for service in SERVICES:
        try:
            response = requests.get(service, timeout=3)

            if response.status_code == 200:
                results[service] = {
                    "status": "UP",
                    "status_code": response.status_code
                }
            else:
                results[service] = {
                    "status": "DOWN",
                    "status_code": response.status_code
                }
        except requests.exceptions.RequestException as e:
            results[service] = {
                "status": "DOWN",
                "error": str(e)
            }
    return results

# /health Route
@app.route("/health", methods=["GET"])
def health():
    return jsonify(check_services())

if __name__ == "__main__":
    app.run(debug=True)
