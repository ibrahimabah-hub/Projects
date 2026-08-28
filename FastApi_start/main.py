from fastapi import FastAPI, HTTPException
from items import Item

app = FastAPI()





items = []


@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items", response_model=list[str])
def list_items(limit:int=10):
    return [item.text for item in items[:limit]]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int)-> Item:
    if 0 <= item_id < len(items):
        item = items[item_id]
        return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    