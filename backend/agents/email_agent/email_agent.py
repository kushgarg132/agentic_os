from ..state import AgentState
from tools.gmail_tools import read_recent_emails, send_email_tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import AIMessage
from config import settings

def email_agent_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4-turbo", api_key=settings.OPENAI_API_KEY)
    tools = [read_recent_emails, send_email_tool]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Email Agent. You handle reading and sending emails. "
                   "You have access to the user's Gmail to list and send emails. "
                   "Always use the provided tools to interact with Gmail. "
                   "The user_id is {user_id}."),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    response = agent_executor.invoke({
        "messages": state["messages"],
        "user_id": state["user_id"]
    })
    
    return {"messages": [AIMessage(content=response["output"])]}
