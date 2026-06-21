#react : agent with tools


from langchain.agents import create_agent # built on langgraph
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

template=''' 
answer the following question,
you have access to {tools}

use this format

question: {input}
Thought : think about what to do
action :decide which tool to use
action input : input for tool
observation: result

--repeat if needed--
thought: i know the answer
final answer: answer
'''
model=ChatGoogleGenerativeAI(model='gemini-3.5-flash',api_key=os.getenv('Gemini_api_key'),temperature=0.7,convert_system_message_to_human=True,response_format=template)

def multiply(a: int,b:int)->int:
    '''multiplying two numbers'''
    return a*b    

from langchain_community.tools import DuckDuckGoSearchRun
searching_tool= DuckDuckGoSearchRun()
tools = [searching_tool]
agent=create_agent(
    model=model,
    tools=tools,
    system_prompt="You are an elite research assistant with real-time web capabilities.\n\n"
    "CRITICAL PRESENTATION RULES:\n"
    "1. When answering the user, ALWAYS cite your sources using the clean format provided by your tool.\n"
    "2. Group facts logically and use bulleted lists instead of large paragraphs.\n"
    "3. Keep summaries brief, punchy, and relevant to the user's explicit question"
)

result= agent.invoke({
    'messages':[
        {
            'role':'user',
            'content': 'what are 3 new jobs freshers in ai can do?'
        }
    ]
})
print(result['messages'][-1].content)
