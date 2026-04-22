import logging

logger = logging.getLogger(__name__)

VALID_SIDES = ["BUY", "SELL"]
VALID_TYPES = ["MARKET", "LIMIT"]

class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> str:
    """Validates and normalizes the trading symbol."""
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string.")
    normalized = symbol.strip().upper()
    if len(normalized) < 5:
        logger.warning(f"Symbol '{normalized}' seems shorter than usual Binance pairs.")
    return normalized

def validate_side(side: str) -> str:
    """Validates the order side."""
    normalized = side.strip().upper()
    if normalized not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of: {VALID_SIDES}")
    return normalized

def validate_order_type(order_type: str) -> str:
    """Validates the order type."""
    normalized = order_type.strip().upper()
    if normalized not in VALID_TYPES:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of: {VALID_TYPES}")
    return normalized

def validate_quantity(quantity: float) -> float:
    """Validates the order quantity."""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a positive number.")

def validate_price(price: float, order_type: str) -> float:
    """Validates the price, particularly for LIMIT orders."""
    if order_type == "MARKET":
        return None # Price is ignored for market orders

    if price is None:
        raise ValidationError("Price is required for LIMIT orders.")

    try:
        p = float(price)
        if p <= 0:
            raise ValueError
        return p
    except (ValueError, TypeError):
        raise ValidationError("Price must be a positive number.")
