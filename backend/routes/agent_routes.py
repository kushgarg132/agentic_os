from fastapi import APIRouter, Depends
from agents.executive.executive_agent import app as agent_app
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: int = 1

@router.post("/chat")
def chat(request: ChatRequest):
    response = agent_app.invoke({
        "messages": [HumanMessage(content=request.message)],
        "user_id": request.user_id,
        "next_agent": ""
    })
    return {"response": response["messages"][-1].content}
