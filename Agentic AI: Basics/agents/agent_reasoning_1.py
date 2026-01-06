from agno.agent import Agent
from agno.models.google import Gemini

from dotenv import load_dotenv


load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    reasoning=True
)

agent.print_response("How much time will it take for a car to travel from Kolkata to Moscow?",
                     stream=True)
