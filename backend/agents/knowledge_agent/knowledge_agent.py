from ..state import AgentState
from tools.drive_tools import search_drive_files
from tools.send_drive_file_tool import send_drive_file_via_email
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import AIMessage
from config import settings

def knowledge_agent_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4-turbo", api_key=settings.OPENAI_API_KEY)
    tools = [search_drive_files, send_drive_file_via_email]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are the Knowledge Agent. You handle searching and managing files in Google Drive. "
                   "You also have the ability to send Drive files via email. "
                   "Always use the provided tools to interact with Drive. "
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
