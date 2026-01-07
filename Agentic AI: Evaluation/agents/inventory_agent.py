from dotenv import load_dotenv

load_dotenv()

from typing import Optional

from agno.agent import Agent
from agno.models.groq import Groq

# ------------------ Inventory Tool (Mock) ------------------
def inventory_tool(product_name):
    """Check inventory status for a product.
    
    Args:
        product_name: The name of the product to check.
        
    Returns:
        str: A string containing stock status and available items count.
             Format: "In Stock: Available Items = N" or "Out of Stock: Available Items = 0"
             or "Product not found in inventory." if product doesn't exist.
    """
    inventory = {
        "iPhone 15": "In Stock: Available Items = 2",
        "AirPods Pro": "Out of Stock: Available Items = 0",
        "MacBook Air M3": "In Stock: Available Items = 5"
    }
    return inventory.get(product_name, "Product not found in inventory.")
    

# ------------------ Inventory Agent ------------------
inventory_agent = Agent(
    name="Inventory Agent",
    model=Groq(id="qwen/qwen3-32b"),
    tools=[inventory_tool],
    instructions=["""
    You are an inventory assistant.

    - If a question is out of scope which is not related to inventory then just say "Sorry, I can't assist with that."
    
    When a user asks about a product, use the inventory_tool to fetch the inventory data.

    - Always call the inventory_tool with the full product name.
    - inventory_tool returns a string (e.g., "In Stock: Available Items = 2") which you need to parse to extract stock status and item counts.
    - Respond with clear, concise information including:
        1. The stock status (e.g., "In Stock", "Out of Stock")
        2. The number of available items (if applicable)
    - If the product is not found, say: "The product is not available in our inventory."

    Never guess or hallucinate information. Do not respond unless the inventory_tool is called.
    Keep your response short and informative.
    """],
    tool_choice="auto",
    markdown=True,
)

if __name__ == "__main__":
    inventory_agent.print_response("I want to buy AirPods Pro, is it available?", stream=False)
