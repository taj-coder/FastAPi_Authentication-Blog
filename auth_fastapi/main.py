# run :  uv run uvicorn main:app --reload  

from fastapi import FastAPI, status
import models
from database import engine
from routers import posts, users, auth  

models.Base.metadata.create_all(bind=engine)  # databse table to python class conversationn & db connection with bind=enigne

app = FastAPI(title="FastAPI Authentication")

# Register routers
app.include_router(auth.router)  
app.include_router(posts.router)
app.include_router(users.router)

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Authentication is now active!"}
