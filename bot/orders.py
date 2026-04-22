import logging
from .client import BinanceFuturesClient

logger = logging.getLogger(__name__)

class OrderManager:
    """High-level order logic for Binance Futures."""
    
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        """
        Places an order (Market or Limit) on Binance Futures.

        Args:
            symbol (str): The trading pair (e.g., BTCUSDT).
            side (str): "BUY" or "SELL".
            order_type (str): "MARKET" or "LIMIT".
            quantity (float): The amount to trade.
            price (float, optional): The limit price. Required if order_type is LIMIT.
            
        Returns:
            dict: The API response payload.
        """
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC" # Good Till Canceled is usually required for LIMIT
            
        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}...")
        
        # Testnet API call to place order
        try:
            response = self.client.request(method="POST", endpoint=endpoint, signed=True, params=params)
            
            logger.info("Order placement successful.")
            return response
            
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            raise
