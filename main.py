from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?"),
]
modelo_version = "gpt-4o"
modelo = ChatOpenAI(model=modelo_version) 
response = modelo.invoke(messages)
print(response.content)
