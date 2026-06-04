from certifi import contents        
import os

from dotenv import load_dotenv
from google import genai
load_dotenv()

client = genai.Client(api_key=os.getenv('gemini_key'))


user_input=input("enter your question:")

    
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_input
        )
print(response.text)
