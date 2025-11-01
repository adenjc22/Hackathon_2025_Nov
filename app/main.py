from fastapi import FastAPI, Depends
from app import auth

app = FastAPI(title="Login Page")

app.include_router(auth.router)

@app.get("/")
def index():
    return {"Login"}

