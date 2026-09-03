from fastapi import FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str = None):
    for item in fake_items_db:
        if item["item_name"] == item_id:
            return item
   
    
    return {"message": "Item not found"}