# we can create reAct agents using langgraph in 2 ways:
#1: using langchain.agents, 2: using state graph
#1:
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

template=''' 
You are a helpful assistant with access to the following tools. 

{tools}

To use a tool, please use the following format:

Thought: You should always think about what to do.
Action: The action to take, exactly one of [{tool_names}]
Action Input: The input to the action
Observation: The result of the action
... (this Thought/Action/Action Input/Observation can repeat multiple times)

Thought: I now know the final answer.
Final Answer: The final answer to the original input question.'''

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

#2: using state graphs

from typing import Annotated,Literal,Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage,SystemMessage
from langchain_core.tools.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

tools = [multiply]
tool_node = ToolNode(tools)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

def agent_node(state: AgentState):
    return {"messages": [model.invoke([SystemMessage(content="Use tools when needed.")] + state["messages"])]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    return "tools" if state["messages"][-1].tool_calls else "__end__"


workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")
app = workflow.compile()

for chunk in app.stream({"messages": [("user", "What is 7 * 8?")]}, stream_mode="values"):
    chunk["messages"][-1].pretty_print()


