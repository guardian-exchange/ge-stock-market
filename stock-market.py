from flask import Flask, jsonify, request
import threading
import time
import random

app = Flask(__name__)

# Set a fixed seed for reproducibility
random.seed(42)

# Multiple stocks
stock_data = {
    "ACME": {"price": 100.0, "volatility": 0.02},
    "GLOBEX": {"price": 150.0, "volatility": 0.03},
    "INITECH": {"price": 200.0, "volatility": 0.01},
    "Hooli": {"price": 90.0, "volatility": 0.025}
}

lock = threading.Lock()


def simulate_stock_prices():
    while True:
        time.sleep(0.5)
        with lock:
            for symbol, data in stock_data.items():
                change_percent = random.gauss(0.0, data["volatility"])
                data["price"] *= (1 + change_percent)
                data["price"] = round(data["price"], 2)


@app.route('/price', methods=['GET'])
def get_price():
    symbol = request.args.get('symbol')
    with lock:
        if symbol:
            if symbol in stock_data:
                return jsonify({symbol: stock_data[symbol]["price"]})
            else:
                return jsonify({"error": f"Symbol '{symbol}' not found"}), 404
        else:
            return jsonify({s: data["price"] for s, data in stock_data.items()})


if __name__ == '__main__':
    thread = threading.Thread(target=simulate_stock_prices, daemon=True)
    thread.start()

    app.run(host='0.0.0.0', port=5000)
