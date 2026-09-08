from pydantic import BaseModel

class Visitor(BaseModel):
    ip_address: str
    visitor_id: int
    visit_id: int

class Visit(BaseModel):
    visit_id: int
    visitor_id: int
    timestamp: str
    page_url: str
    