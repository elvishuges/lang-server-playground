from dotenv import load_dotenv
import os

print("Hello, VS Code!")
def greet(name):
    return f"Hello, {name}!"
if __name__ == "__main__":
    name = input("Enter your name: ")
    print(greet(name))