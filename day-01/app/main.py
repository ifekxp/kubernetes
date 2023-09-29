# main.py

from fastapi import FastAPI
from datetime import datetime
import socket

app = FastAPI()

@app.get("/")
async def root():
    current_time = str(datetime.now())
    hostname = socket.gethostname()

    message = "time: " + current_time + ", host: " + hostname

    return {"response": message}

@app.get("/liveness")
def health():
    return "Ok"  

@app.get("/readiness")
def health():
    return "Ok"  