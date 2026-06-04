import os
from google import genai
from dotenv import load_dotenv
from certifi import contents


load_dotenv()

client=genai.Client(api_key=os.getenv('api_key'))

audio_file=client.files.upload( file='SUPERDATASCIENCE_pdcast.mp3')

response=client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[audio_file,
              '''summarize the podcast by highlighting key points'''
]
)
print(response.text)