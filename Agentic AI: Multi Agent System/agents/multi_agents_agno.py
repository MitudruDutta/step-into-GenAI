from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.team import Team

# Simulated inventory lookup tool
def check_inventory(product_name: str) -> str:
    """Check the inventory status for a given product.
    
    Args:
        product_name (str): The name of the product to check.
        
    Returns:
        str: The inventory status of the product.
    """
    inventory = {
        "iPhone 15": "In stock (Ships in 2 days)",
        "AirPods Pro": "Out of stock (Available in 2 weeks)",
        "MacBook Air M3": "Low stock (Only 3 left!)",
    }
    return inventory.get(product_name, "Product not found in inventory.")

# Agent 1: Handles customer FAQs and policy questions
faq_agent = Agent(
    name="FAQ Agent",
    role="Answer customer questions using web search",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[DuckDuckGoTools()],
    instructions="Answer e-commerce related queries using web search. Use Best Buy store if someone is asking about electronics. Include source if possible.",
    tool_choice="auto",
    markdown=True,
)

# Agent 2: Checks product stock availability
inventory_agent = Agent(
    name="Inventory Agent",
    role="Check inventory for a given product",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[check_inventory],
    instructions="Only respond with inventory status of the product.",
    tool_choice="auto",
    markdown=True,
)

# Multi-agent team coordination
support_team = Team(
    role="coordinate",
    members=[faq_agent, inventory_agent],
    model=Groq(id="llama-3.1-8b-instant"),
    instructions=["Be polite", "Include product availability and any relevant policies"],
    tool_choice="auto",
    markdown=True,
)


if __name__ == "__main__":
    # Sample query
    support_team.print_response(
        "Is the iPhone 15 in stock? Also, what's your return policy on electronics?",
        stream=True
    )
