# Cart to store items
mcp_cart = {}

def add_item(key: str, quantity: int) -> str:
    """Add an item to the cart with specified quantity"""
    mcp_cart[key] = quantity
    return f"Added {key} with quantity: {quantity}"


def get_items() -> dict:
    """Get all items from the cart"""
    return {"items": mcp_cart}


def remove_item(key: str) -> str:
    """Remove an item from the cart"""
    if key in mcp_cart:
        value = mcp_cart.pop(key)
        return f"Removed {key}: {value}"
    return f"Key {key} not found"
