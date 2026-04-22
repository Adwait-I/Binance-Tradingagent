import argparse
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure the local bot package can be accessed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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

def main():
    # Setup structured logging first
    setup_logging()
    logger = logging.getLogger(__name__)

    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # We enforce keys during runtime, but the CLI parsing can happen first
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders (required if type is LIMIT)")
    
    args = parser.parse_args()

    # CLI Output formatting functions
    def print_summary(msg, is_error=False):
        separator = "=" * 50
        print(f"\n{separator}")
        if is_error:
            print(f"❌ ERROR: {msg}")
        else:
            print(f"✅ SUCCESS: {msg}")
        print(f"{separator}\n")

    print("\n--- Order Request Summary ---")
    print(f"Symbol:   {args.symbol.upper()}")
    print(f"Side:     {args.side.upper()}")
    print(f"Type:     {args.type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.type.upper() == "LIMIT":
        print(f"Price:    {args.price}")
    print("-----------------------------\n")

    # Validate Inputs Before API Call
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValidationError as e:
        logger.error(f"Input validation failed: {str(e)}")
        print_summary(f"Validation Error: {str(e)}", is_error=True)
        sys.exit(1)

    # Validate Credentials
    if not api_key or not api_secret:
        msg = "Missing Binance API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in the environment or a .env file."
        logger.error(msg)
        print_summary(msg, is_error=True)
        sys.exit(1)

    # Initialize Client and Manager
    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, testnet=True)
        manager = OrderManager(client)
    except Exception as e:
        logger.error(f"Initialization Error: {e}")
        print_summary(f"Initialization Error: {e}", is_error=True)
        sys.exit(1)

    # Place Order
    print("Sending order to Binance Futures Testnet...")
    try:
        response = manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Display response details
        print_summary("Order Placed Successfully!")
        print("--- Order Response Details ---")
        print(f"Order ID:      {response.get('orderId', 'N/A')}")
        print(f"Status:        {response.get('status', 'N/A')}")
        print(f"Executed Qty:  {response.get('executedQty', 'N/A')}")
        avg_price = response.get('avgPrice')
        if avg_price and float(avg_price) > 0:
            print(f"Avg Price:     {avg_price}")
        elif order_type == "LIMIT":
            print(f"Target Price:  {response.get('price', 'N/A')}")
        
        print("\nFull details have been written to trading_bot.log.")
        
    except Exception as e:
        print_summary(f"Order Placement Failed! Check log for details.", is_error=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
