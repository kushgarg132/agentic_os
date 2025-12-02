from ..state import AgentState
from tools.calendar_tools import list_events_tool, create_event_tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from config import settings

def planner_agent_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4-turbo", api_key=settings.OPENAI_API_KEY)
    tools = [list_events_tool, create_event_tool]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Planner Agent. You handle calendar events and scheduling. "
                   "You have access to the user's calendar to list and create events. "
                   "Always use the provided tools to interact with the calendar. "
                   "The user_id is {user_id}."),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    # Filter messages to only include those relevant to the conversation history
    # For simplicity, we pass the full history, but in production we might want to trim it
    response = agent_executor.invoke({
        "messages": state["messages"],
        "user_id": state["user_id"]
    })
    
    return {"messages": [AIMessage(content=response["output"])]}
