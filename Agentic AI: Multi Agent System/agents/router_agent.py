from dotenv import load_dotenv
load_dotenv()

import re
from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team


# ------------------ Shared Helper for Word-Boundary Matching ------------------
def match_keyword_response(query: str, responses: dict) -> str | None:
    """Match keywords using word-boundary regex to avoid false positives.
    
    Args:
        query: The user query to search in.
        responses: Dict mapping keywords to responses.
        
    Returns:
        The matched response or None if no match found.
    """
    query_lower = query.lower()
    for keyword, response in responses.items():
        # Use word boundary matching to avoid false positives
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, query_lower, re.IGNORECASE):
            return response
    return None


# ------------------ Tool 1: Technical Support Tool ------------------
def technical_support(query: str) -> str:
    """Handle technical support queries.
    
    Args:
        query (str): The technical support question or issue description.
        
    Returns:
        str: A helpful response to the technical issue.
    """
    responses = {
        "app crash": "Please try reinstalling the app and update your OS.",
        "login issue": "Try resetting your password using the 'Forgot Password' link.",
        "freezing": "Clear the app cache and restart your device.",
    }
    result = match_keyword_response(query, responses)
    return result if result else "Please provide more details about the technical issue."


# ------------------ Tool 2: Sales Support Tool ------------------
def sales_support(query: str) -> str:
    """Handle sales and pricing queries.
    
    Args:
        query (str): The sales or pricing question.
        
    Returns:
        str: Information about pricing, discounts, or sales.
    """
    responses = {
        "cost": "Our premium plan costs $49.99/month with 24/7 support.",
        "discount": "Yes! We are offering 20% off for new users this week.",
        "pricing": "We have Basic, Pro, and Premium plans starting at $9.99/month.",
    }
    result = match_keyword_response(query, responses)
    return result if result else "Let me connect you to a sales representative for more details."


# ------------------ Tool 3: General Inquiry Tool ------------------
def general_info(query: str) -> str:
    """Handle general information queries.
    
    Args:
        query (str): The general information question.
        
    Returns:
        str: General information about business hours, location, or contact details.
    """
    responses = {
        "hours": "We are open from 9 AM to 6 PM, Monday to Friday.",
        "location": "Our headquarters are located in San Francisco, CA.",
        "contact": "You can contact us at support@example.com or call 1800-123-456.",
    }
    result = match_keyword_response(query, responses)
    return result if result else "Can you clarify your question? I'm here to help."


# ------------------ Agent 1: Technical Support Agent ------------------
tech_agent = Agent(
    name="Tech Support Agent",
    role="Handle technical issues",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[technical_support],
    instructions="Use the technical support tool to answer user queries. Keep responses helpful and simple. Provide them direct answer using the tool, do not ask further questions. Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)

# ------------------ Agent 2: Sales Agent ------------------
sales_agent = Agent(
    name="Sales Agent",
    role="Handle pricing and sales questions",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[sales_support],
    instructions="Use the sales tool to answer pricing and discount-related questions. Provide them direct answer using the tool, do not ask further questions. Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)

# ------------------ Agent 3: General Inquiry Agent ------------------
general_agent = Agent(
    name="General Inquiry Agent",
    role="Answer general questions like hours, location, and contact info",
    model=Groq(id="llama-3.1-8b-instant"),
    tools=[general_info],
    instructions="Use the general info tool to help with common inquiries. Provide them direct answer using the tool, do not ask further questions. Provide short answer in less than two lines.",
    tool_choice="auto",
    markdown=True,
)

# ------------------ Router Team ------------------
router_team = Team(
    name="Customer Care Chatbot Agent",
    role="route",
    members=[tech_agent, sales_agent, general_agent],
    model=Groq(id="llama-3.1-8b-instant"),
    instructions="Route the query to the correct agent based on whether it's technical, sales, or general.",
    tool_choice="auto",
    markdown=True,
    show_members_responses=True,
)


# ------------------ Main Entry Point ------------------
if __name__ == "__main__":
    print("\n--- TEST: SALES ---")
    router_team.print_response("Do you have any ongoing discounts on the premium plan?", stream=True)
    
    # Uncomment to run other tests:
    # print("\n--- TEST: TECHNICAL ---")
    # router_team.print_response("My app keeps freezing whenever I try to open settings.", stream=True)
    
    # print("\n--- TEST: GENERAL INFO ---")
    # router_team.print_response("What are your business hours on weekdays?", stream=True)
