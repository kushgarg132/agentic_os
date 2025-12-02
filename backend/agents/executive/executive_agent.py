from langgraph.graph import StateGraph, END
from .state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import settings

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

class Router(BaseModel):
    """Route the user's request to the appropriate agent."""
    next_agent: Literal["email_agent", "knowledge_agent", "planner_agent", "end"] = Field(
        ..., description="The next agent to route the request to. 'end' if the task is complete or no agent is suitable."
    )

def executive_node(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY)
    structured_llm = llm.with_structured_output(Router)
    
    system_prompt = (
        "You are the Executive Agent. Your job is to route the user's request to the appropriate specialist agent.\n"
        "Available agents:\n"
        "- email_agent: Handles reading and sending emails.\n"
        "- knowledge_agent: Handles searching Google Drive files and sending them via email.\n"
        "- planner_agent: Handles calendar events and scheduling.\n"
        "If the request is simple greeting or the task is completed, route to 'end'."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])
    
    chain = prompt | structured_llm
    
    last_message = state['messages'][-1]
    result = chain.invoke({"input": last_message.content})
    
    return {"next_agent": result.next_agent}

from ..email_agent.email_agent import email_agent_node
from ..knowledge_agent.knowledge_agent import knowledge_agent_node
from ..planner_agent.planner_agent import planner_agent_node

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("executive", executive_node)
workflow.add_node("email_agent", email_agent_node)
workflow.add_node("knowledge_agent", knowledge_agent_node)
workflow.add_node("planner_agent", planner_agent_node)

workflow.set_entry_point("executive")

workflow.add_conditional_edges(
    "executive",
    lambda x: x["next_agent"],
    {
        "email_agent": "email_agent",
        "knowledge_agent": "knowledge_agent",
        "planner_agent": "planner_agent",
        "end": END
    }
)

workflow.add_edge("email_agent", END)
workflow.add_edge("knowledge_agent", END)
workflow.add_edge("planner_agent", END)

app = workflow.compile()
