from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from pydantic import BaseModel
from database.database import Base
from datetime import datetime
from typing import List

class Visitor(Base):
    __tablename__ = 'visitor'

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True)

class Visit(Base):
    __tablename__ = 'visit'

    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Float, index=True, default=0)
    visitor_id = Column(Integer, ForeignKey("visitor.id"))

class Hit(Base):
    __tablename__ = 'hit'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    page_url = Column(String, index=True)
    visit_id = Column(Integer, ForeignKey("visit.id"))

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    brand  = Column(String, index=True)
    price  = Column(Float, index=True)

class VisitorBase(BaseModel):
    ip_address: str
    visits: List[VisitBase]

class VisitBase(BaseModel):
    duration: float
    hits: List[HitBase] 


class HitBase(BaseModel):
    page_url: str
    timestamp: datetime