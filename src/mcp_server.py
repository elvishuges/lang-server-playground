from fastmcp import FastMCP
from src.tools import (
    add_item as tools_add_item,
    get_items as tools_get_items,
    remove_item as tools_remove_item
)

mcp = FastMCP("MCP_STORE")


class MCPServer:
    def add_item(self, key: str, quantity: int) -> str:
        return tools_add_item(key, quantity)

    def get_items(self) -> dict:
        return tools_get_items()

    def remove_item(self, key: str) -> str:
        return tools_remove_item(key)


server = MCPServer()

mcp.tool(server.add_item)
mcp.tool(server.get_items)
mcp.tool(server.remove_item)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)