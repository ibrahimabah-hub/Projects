from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import database.models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from database.models import HitBase, VisitorBase, VisitBase
from datetime import datetime

app = FastAPI()
database.models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/visitors/{visitor_id}")
async def get_visitor_by_id(visitor_id: int, db: db_dependency):
    result = db.query(database.models.Visitor).filter(database.models.Visitor.id == visitor_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return result

@app.get("/visitors/")
async def get_visitors(db: db_dependency):
    result = db.query(database.models.Visitor).all()
    if not result:
        raise HTTPException(status_code=404, detail="No visitors not found")
    return result

@app.get("/visits/{visitor_id}")
async def get_visits_by_id(visitor_id: int, db: db_dependency):
    result = db.query(database.models.Visit).filter(database.models.Visit.visitor_id == visitor_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return result

@app.get("/visits/")
async def get_visits(db: db_dependency):
    result = db.query(database.models.Visit).all()
    if not result:
        raise HTTPException(status_code=404, detail="No visitors not found")
    return result

@app.post("/visitors/")
async def create_visitor(visitor: VisitorBase, db: db_dependency):
    db_visitor = database.models.Visitor(ip_address=visitor.ip_address)
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    for visit in visitor.visits:
        if len(visit.hits)>1:
            visit.duration = (visit.hits[-1].timestamp - visit.hits[0].timestamp).total_seconds()
        else:
            visit.duration = 0
        db_visit = database.models.Visit(visitor_id=db_visitor.id, duration=visit.duration)
        db.add(db_visit)
        db.commit()
        for hit in visit.hits:
            db_hit = database.models.Hit(page_url=hit.page_url, timestamp=hit.timestamp, visit_id=db_visit.id)
            db.add(db_hit)
        db.commit()
    db.commit()
