#used different memory strategies
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
history=InMemoryChatMessageHistory()
from langchain_core.prompts import ChatPromptTemplate

model=ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=os.getenv('Gemini_api_key'),temperature=0.7,convert_system_message_to_human=True)

#sliding window: only preserves the top k, as inefficient as it sounds
#summarization: uses an llm to seperately summarize the history

history=InMemoryChatMessageHistory()
summary=''
max_msg=10

def get_message():
    msg=[SystemMessage(content='you are a witty,sometimes cheesy model, help out the user with their queries using less than 10 words ')]
    if summary:
        msg.append(SystemMessage(content=f"Conversation summary: {summary}"))
    msg+=history.messages
    return msg
while True:
    que=input('you:')
    if que.lower()=='q':
        break
    history.add_user_message(que)
    response=model.invoke(get_message())
    history.add_ai_message(response.content)
    print("bot:",response.content)
    if len(history.messages)> max_msg:
        summarization=ChatPromptTemplate.from_messages([
            ("system",
             "Summarize the conversation. "
             "Keep important facts, user preferences, goals, questions, and answers."),
            ("user","{chat}")
        ])
        summary_chain=summarization| model
        result=summary_chain.invoke({'chat':history.messages})
        summary=result.content
        history.messages=history.messages[-5:]
get_message()