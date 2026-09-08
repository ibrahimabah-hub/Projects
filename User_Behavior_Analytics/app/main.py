from fastapi import FastAPI, HTTPException, Path, Query, Depends
from db.visitor import Visitor, Visit
from datetime import datetime


app = FastAPI()

session_1 = {'id': 1, 'userid': 1, 'start_time': '2023-01-01 10:00:00', 'end_time': '2023-01-01 11:00:00', 'metadata': {}}

def get_settings():
    return {"env": "dev", "version": "0.1.0"}

@app.get("/visit")
def get_visit(session: dict | None = Depends(lambda: session_1)):
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"visitor": "you", 
            "visit": "existing",
            "start_time": session["start_time"],
            "end_time": session["end_time"],
            "metadata": session["metadata"]}

@app.get("/visit/new")
def new_visitor(settings: dict = Depends(get_settings)):
    return {"visitor": "you", 
            "visit": "new",
            "env": settings["env"],
            "version": settings["version"]}

'''@app.post("/visitors")
def create_visitor(visitor: Vistitor):'''