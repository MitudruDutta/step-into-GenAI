from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os
import sys


load_dotenv()

# Validate required environment variables
if not os.getenv("GROQ_API_KEY"):
    sys.exit("Error: GROQ_API_KEY environment variable is not set. Please add it to your .env file.")

try:
    agent = Agent(
        name="basic-agent",
        model=Groq(id="llama-3.1-8b-instant"),
        tools=[DuckDuckGoTools()],
        description="You are an enthusiastic news reporter with a flair for storytelling.",
        markdown=True
    )
except Exception as e:
    print(f"Error: Failed to initialize agent 'basic-agent' with model 'llama-3.1-8b-instant'.")
    print(f"Details: {type(e).__name__}: {e}")
    sys.exit(1)

agent.print_response("Tell me the latest news about India along with web urls of news sources.")

