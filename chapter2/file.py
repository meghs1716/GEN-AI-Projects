import os
from google import genai
from dotenv import load_dotenv
from certifi import contents


load_dotenv()

client=genai.Client(api_key=os.getenv('api_key'))

with open('test_ai_notes.txt','r',encoding='utf-8') as file:
    content=file.read()
    
response=client.models.generate_content(
    model='gemini-2.5-flash',
    contents='''summarize this file about nlp in 50 words:\n\n{content}'''
)
print(response.text)