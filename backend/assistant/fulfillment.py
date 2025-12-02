from fastapi import APIRouter, Request
from agents.executive.executive_agent import app as agent_app
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/webhook")
async def dialogflow_webhook(request: Request):
    data = await request.json()
    intent = data.get("queryResult", {}).get("intent", {}).get("displayName")
    query_text = data.get("queryResult", {}).get("queryText")
    
    # Extract user_id from session or context (simplified)
    user_id = 1 
    
    if intent == "Agent Command":
        # Pass to Executive Agent
        response = agent_app.invoke({
            "messages": [HumanMessage(content=query_text)],
            "user_id": user_id,
            "next_agent": ""
        })
        
        ai_message = response["messages"][-1].content
        
        return {
            "fulfillmentText": ai_message
        }
    
    return {
        "fulfillmentText": "I'm not sure how to handle that."
    }
