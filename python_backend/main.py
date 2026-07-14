from fastapi import FastAPI
from agent.requests import router as agent
app = FastAPI(title="Agent")
app.include_router(agent)   