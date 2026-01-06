from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv


load_dotenv()

def get_stock_symbol(company_name):
    """Use this function to get the symbol for a company.

    Args: 
        company_name (str): The name of the company.

    Returns:
        str: The stock symbol of the company.
    """
    symbols = {
        "AtliQ": "MSFT",  # Placeholder: AtliQ is a fictional company used for demo purposes
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Amazon": "AMZN"
    }
    return symbols.get(company_name, company_name)


agent = Agent(
    name="Finance Agent",
    model=Groq(id="qwen/qwen3-32b"),
    tools=[YFinanceTools(include_tools=["get_current_stock_price", "get_analyst_recommendations", "get_company_info"]), get_stock_symbol],
    instructions=[
        "You are a financial expert AI agent. Use the provided tools to assist users with their financial inquiries.",
        "Use get_stock_symbol only for companies not in your knowledge base. For well-known public companies (e.g., NVIDIA, Apple, Tesla), you may infer the symbol directly."
    ],
    tool_choice="auto",
    markdown=True
)

agent.print_response("What is the current stock price of NVIDIA?")