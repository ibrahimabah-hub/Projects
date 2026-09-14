from enum import Enum
from datetime import date, datetime
from pydantic import BaseModel, field_validator, model_validator
from sqlmodel import SQLModel, Field, Relationship

class VisitorBase(SQLModel):
    ip_address: str | None = Field(default=None, nullable=True)
    #visit_id: int = Field(default=None, foreign_key="visit.id", nullable=True)

class VisitBase(SQLModel):
    #visitor_id: int = Field(default=None, foreign_key="visitor.id", nullable=True)
    duration: float
    

class HitBase(SQLModel):
    hit_id: int
    #visit_id: int = Field(default=None, foreign_key="visit.id", nullable=True)
    #visitor_id: int = Field(default=None, foreign_key="visitor.id", nullable=True)
    timestamp: datetime = Field(default=datetime.today())
    page_url: str
    #product_id: int | None = Field(default=None, foreign_key="product.id", nullable=True)

class ProductBase(SQLModel):
    product_id: int
    type: str 
    brand: str
    form_factor: str
    category: str
    price: float

class Visitor(VisitorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    visits: list[Visit] | None = Relationship(back_populates="visitor")

class Visit(VisitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    visitor_id: int = Field(default=None, foreign_key="visitor.id", nullable=False)
    visitor: Visitor = Relationship(back_populates="visits")
    hits: list[Hit] = Relationship(back_populates="visit")
    duration: float = Field(default=0.0)
    @model_validator(mode="after")
    def compute_duration(self):
        if not self.hits or len(self.hits) < 2:
            return self
            #raise ValueError("At least two hits are required to compute duration")

        duration = self.hits[-1].timestamp - self.hits[0].timestamp

        if duration.total_seconds() < 0:
            raise ValueError("Duration cannot be negative")

        self.duration = duration.total_seconds()
        return self

class Hit(HitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visit.id")
    visit: Visit = Relationship(back_populates="hits")
    visitor_id: int = Field(foreign_key="visitor.id")
    product_id: int | None = Field(default=None, foreign_key="product.id", nullable=True)
    

class Product(ProductBase, table=True):
    id: int = Field(default=None, primary_key=True)

class VisitorCreate(SQLModel):
    ip_adress: str | None = None
    visits: list["VisitCreate"] | None = None

class VisitCreate(SQLModel):
    hits: list["HitCreate"]

class HitCreate(SQLModel):
    hit_id: int
    timestamp: datetime
    page_url: str
    product_id: int | None = None