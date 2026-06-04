import os
from PIL import Image
from google import genai
from dotenv import load_dotenv
from certifi import contents


load_dotenv()

client=genai.Client(api_key=os.getenv('api_key'))
print(Image)
img=Image.open('image.png')
response=client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[img,'''Analyze this image.

    1. Describe what you see.
    2. Are there any signs it may be AI-generated?
    3. How confident are you?
    4. Explain your reasoning.
    ''']
)
print(response.text)