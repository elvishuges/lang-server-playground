from typing import Any
import asyncio
import json
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

# ✅ use variável de ambiente (NÃO hardcode)
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key  

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


async def main(query: str):
    """Main function to process queries using the MCP client."""
    client = MultiServerMCPClient({
        "mcpstore": {
            "url": "http://127.0.0.1:8001/mcp",
            "transport": "streamable_http"
        }
    })

    tools = await client.get_tools()

    agent = create_agent(
    model,
    tools,
    system_prompt="""
    Você é um assistente que analisa qual função deve ser chamada com base na solicitação do usuário.
    """
)

    response = await agent.ainvoke({
    "messages": [
        {"role": "user", "content": query}
    ]
})

    return response


def serialize_response(obj: Any) -> Any:
    """Helper function to make the response JSON serializable."""
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)


def print_tool_calls(response):
    for message in response.get("messages", []):
        tool_calls = getattr(message, "tool_calls", None)

        if tool_calls:
            print("\n------------Tool Calls------------")
            for tool_call in tool_calls:
                print(f"Tool Name: {tool_call.get('name')}")
                print(f"Tool ID: {tool_call.get('id')}")
                print("Arguments:", json.dumps(tool_call.get("args"), indent=2))
                print("------------------------")


def print_ai_messages(response):
    """Print all non-empty AI messages from the response."""
    for message in response["messages"]:
        if type(message).__name__ == "AIMessage" and message.content:
            print("\n------------AI Message------------")
            print(f"Content: {message.content}")
            print("--------------------------------")

def process_and_print_response(response):
        """Process and print the response from the agent."""
        #json_response = json.dumps(response, default=serialize_response, indent=2)
        #print("\n------------Json Response------------")
        #print(json_response)
        print_tool_calls(response)   
        print_ai_messages(response)



# ✅ resolve o erro de event loop
async def run_all():
    item = "apple"
    quantity = 3

    print("\n------------Adding------------")
    response = await main(f"Add an item {item} of quantity {quantity} to mcpstore website cart")
    process_and_print_response(response)

    print("\n------------Getting------------")
    response = await main("Get the mcpstore website cart contents")
    process_and_print_response(response)

    print("\n------------Removing------------")
    response = await main(f"Remove the item {item} from mcpstore website cart")
    process_and_print_response(response)

    print("\n------------Getting again------------")
    response = await main("Get the mcpstore website cart contents")
    process_and_print_response(response)


async def interactive():
    print("\n🤖 Modo interativo iniciado (digite 'sair' para encerrar)\n")

    while True:
        query = input("👉 Você: ").strip()

        if query.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break

        if not query:
            print("⚠️ Digite algo válido")
            continue

        try:
            response = await main(query)
            process_and_print_response(response)

        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(interactive())
