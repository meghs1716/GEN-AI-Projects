from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash',convert_system_message_to_human=True,api_key=os.getenv('Gemini_api_key'))

from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel,Field
class Country(BaseModel):
    continent:str=Field(description=('what continent the country belongs to'))
    independent_since:int=Field(description=('when did the country get independence'))
    population:int=Field(description=('how many people live in the country'))
    
structured_model=model.with_structured_output(Country)

prompt=ChatPromptTemplate.from_messages([
    ('system','answer the query only with the format, only answer in one sentence each'),
    ('user','{que}')
])

chain=prompt | structured_model
response=chain.invoke({'que':'japan'})
print(response)