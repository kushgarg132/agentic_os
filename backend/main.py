from fastapi import FastAPI
from config import settings
from db.database import engine, Base
from routes import auth_routes, agent_routes
from assistant.fulfillment import router as assistant_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(agent_routes.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(assistant_router, prefix="/api/v1/assistant", tags=["assistant"])

@app.get("/")
def root():
    return {"message": "Agentic AI OS is running"}
