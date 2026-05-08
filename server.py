import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TRADIER_API_KEY = os.getenv("TRADIER_API_KEY")
TRADIER_ACCOUNT_ID = os.getenv("TRADIER_ACCOUNT_ID")
ENVIRONMENT = os.getenv("ENVIRONMENT", "demo")

TRADIER_URL = "https://sandbox.tradier.com/v1/accounts/{}/orders".format(TRADIER_ACCOUNT_ID)

@app.route("/", methods=["GET"])
def home():
    return "Spy-Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    symbol = data.get("symbol")
    side = data.get("side")
    qty = int(os.getenv("POSITION_SIZE", 1))

    headers = {
        "Authorization": f"Bearer {TRADIER_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "class": "equity",
        "symbol": symbol,
        "side": side,
        "quantity": qty,
        "type": "market",
        "duration": "day"
    }

    r = requests.post(TRADIER_URL, headers=headers, data=payload)
    return jsonify({"status": "ok", "tradier_response": r.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
