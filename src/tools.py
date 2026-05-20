# Cart to store items
mcp_cart = {}

def add_item(key: str, quantity: int) -> str:
    mcp_cart[key] = quantity
    return f"Added {key} with quantity: {quantity}"


def get_items() -> dict:
    return {"items": mcp_cart}


def remove_item(key: str) -> str:
    if key in mcp_cart:
        value = mcp_cart.pop(key)
        return f"Removed {key}: {value}"
    return f"Key {key} not found"
