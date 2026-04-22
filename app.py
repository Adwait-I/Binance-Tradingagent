import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    ValidationError
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load Environment Variabls
load_dotenv()

app = Flask(__name__)

# Initialize Binance client using env vars on startup
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# If keys are missing, we log a warning but still start the app so UI can render
if not api_key or not api_secret:
    logger.warning("Missing BINANCE_API_KEY or BINANCE_API_SECRET. Orders will fail until configured.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    
    if not api_key or not api_secret:
        return jsonify({"success": False, "error": "API keys not configured in environment"}), 400

    try:
        symbol = validate_symbol(data.get("symbol", ""))
        side = validate_side(data.get("side", ""))
        order_type = validate_order_type(data.get("type", ""))
        quantity = validate_quantity(data.get("quantity"))
        price = data.get("price")
        
        # Only validate price if it's not None (for Limit orders) or if the type requires it
        validated_price = validate_price(price, order_type) if order_type == "LIMIT" else None

    except ValidationError as e:
        logger.error(f"UI Input validation failed: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Invalid input format: {str(e)}"}), 400

    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, testnet=True)
        manager = OrderManager(client)
        
        # Attempt to place the order
        response = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=validated_price
        )
        
        return jsonify({
            "success": True,
            "data": response
        })

    except Exception as e:
        logger.error(f"UI Order placement failed: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
