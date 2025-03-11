import os
import openai
from dotenv import load_dotenv
import requests
import json
# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
apikey = os.getenv("api_key")
import requests


# Make the API request
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {apikey}",
    },
    json={
        "model": "deepseek/deepseek-r1:free",  # Use the DeepSeek model
        "messages": [
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    }
)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    response_data = response.json()
    # Extract the generated content
    generated_text = response_data["choices"][0]["message"]["content"]
    print("Generated Text:", generated_text)
else:
    # Handle errors
    print(f"Error: {response.status_code}")
    print("Response:", response.text)
