from agno.agent import Agent
from agno.media import Image
from agno.models.google import Gemini
from dotenv import load_dotenv
from pathlib import Path
import os
import json
import sys

load_dotenv()

def get_item_code(item_name):
    """
    Returns the item code corresponding to the provided item name. If the item
    name does not match any predefined items, a default code is returned.

    :param item_name: The name of the item to retrieve the code for. Expected
                      values are "sari", "t-shirt", "jeans", "jacket".
    :type item_name: str
    :return: The code corresponding to the given item name. Returns "ITM001"
             for "sari", "ITM002" for "t-shirt", "ITM003" for "jeans",
             "ITM004" for "jacket", and "ITM999" for any other input.
    :rtype: str
    """
    if item_name == "sari":
        return "ITM001"

    if item_name == "t-shirt":
        return "ITM002"

    if item_name == "jeans":
        return "ITM003"

    if item_name == "jacket":
        return "ITM004"

    return "ITM999"

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[get_item_code]
)

image_paths = [
    os.path.join(Path(__file__).parent, "images", "image1.jpg"),
    os.path.join(Path(__file__).parent, "images", "image2.jpg"),
    os.path.join(Path(__file__).parent, "images", "image3.jpg")
]

for path in image_paths:
    if not os.path.exists(path):
        print(f"Error: Image file not found at {path}. Please ensure the 'images' directory exists and contains the required files.")
        sys.exit(1)

response = agent.run(
    input='''For each image, generate a JSON record that looks like this:
    {
        "item_name": "sari",
        "item_code": "ITM001",
        "color": "red",
        "gender": "female",
        "age_category": "adult" 
    }
    Output must be a JSON string that Python can parse it directly.
    Do not put any pre-amble instructions or even 'json' in front of the response string.
    item_name should be one of the following: sari, t-shirt, jeans, jacket
    age_category should be one of the following: adult, child 
    ''',
    images=[Image(filepath=p) for p in image_paths]
)

if response.content:
    try:
        print(json.loads(response.content))
    except json.JSONDecodeError:
        print(f"Error: Model did not return valid JSON. Response: {response.content}")
