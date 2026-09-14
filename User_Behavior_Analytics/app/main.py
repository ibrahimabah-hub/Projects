from fastapi import FastAPI, HTTPException, Path, Query, Depends
from sqlmodel import Session, select
from db.db_schema import Visitor, Visit, Hit, Product, VisitCreate, VisitorCreate, HitCreate
from datetime import datetime
from db.db import get_session, init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/visitor/{visitor_id}")
def get_visitor_by_id(visitor_id: int, session = Depends(get_session))->Visitor:
    visitor = session.get(Visitor, visitor_id)
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return visitor

@app.post("/visitor/new")
def create_visitor(new_tor: VisitorCreate, session=Depends(get_session)):
    visitor = Visitor(ip_address=new_tor.ip_adress)
    session.add(visitor)
    session.commit()
    session.refresh(visitor)
    if new_tor.visits:
        vis_obj = []
        for vis in new_tor.visits:
            visit = Visit()
            if vis.hits:
                hit_obj = []
                for hit in vis.hits:
                    h = Hit(hit_id=hit.hit_id, 
                            page_url=hit.page_url, 
                            timestamp=hit.timestamp, 
                            product_id=hit.product_id)



@app.get("/visit/{visit_id}")
def get_visit_by_id(visit_id: int, session = Depends(get_session))-> Visit:
    visit = session.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit
    

@app.post("/visit/new")
def create_visit(new_visit: VisitCreate, session: Session = Depends(get_session))-> Visit:
    
    visitor = Visitor(ip_address="auto")
    session.add(visitor)
    session.commit()
    session.refresh(visitor)

    visit = Visit(visitor_id=visitor.id)
    session.add(visit)
    session.commit()
    session.refresh(visit)
    hit_obs = []
    for h in new_visit.hits:
        hit = Hit(hit_id=h.hit_id, 
                      timestamp=h.timestamp, 
                      page_url=h.page_url,
                      visitor_id=visit.visitor_id,
                      visit_id=visit.id)
        hit_obs.append(hit)
    visit.hits = hit_obs
    session.add(visit)
    session.commit()
    session.refresh(visit)
    return visit


'''@app.post("/visitors")
def create_visitor(visitor: Vistitor):'''