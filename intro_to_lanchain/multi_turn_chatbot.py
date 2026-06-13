import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage
model=ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=os.getenv('Gemini_api_key'),temperature=0.7,convert_system_message_to_human=True)
from langchain_core.chat_history import InMemoryChatMessageHistory
history =InMemoryChatMessageHistory()
sys_msg=SystemMessage(content='you are a rude and snarky ai who only answers in 3-5 words')


def pipeline():
    while True:
        print('welcome, press q to exit')
        question=input('you:').strip()
        if question.lower() =='q':
            break
        response=model.invoke([sys_msg]+history.messages+[HumanMessage(content=question)])
        history.add_user_message(question)
        history.add_ai_message(response)
        print('bot:',response.content)
pipeline()
    
    