from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools


from dotenv import load_dotenv

load_dotenv()


agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(include_tools=["get_current_stock_price", "get_analyst_recommendations", "get_company_info"])
    ],
    instructions=[
        "Use tables to display data",
        "Only output the report, no other text"
    ],
    markdown=True
)


agent.print_response("Write a report on NVDA", stream=True, show_full_reasoning=True, stream_intermediate_steps=True)