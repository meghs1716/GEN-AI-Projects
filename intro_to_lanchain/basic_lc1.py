from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash',convert_system_message_to_human=True,api_key=os.getenv('Gemini_api_key'))

#model creation
from langchain_core.prompts import ChatPromptTemplate
prompt=ChatPromptTemplate.from_messages([
    ('system','you help out the user by providing ans in json format'),
    ('user','what does {que} mean')
])
#user input 
question=input("ask anything you want")
#LCEL
chain=prompt | model
# final response
response=chain.invoke({'que':question})
print(response.content)
