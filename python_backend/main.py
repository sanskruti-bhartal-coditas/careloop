from fastapi import FastAPI
from agent.requests import router as agent
from auth.auth_routes import router as auth
app = FastAPI(title="Agent")
app.include_router(agent)   
app.include_router(auth)