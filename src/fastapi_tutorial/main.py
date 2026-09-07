import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="FastAPI")


class Item(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class CreateItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class UpdateItem(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None


fake_items_db = [
    Item(id=1, name="Foo", price=10.5, tax=1.2),
    Item(id=2, name="Bar", description="A bar item", price=5.2),
    Item(id=3, name="Baz", price=8.0),
    Item(id=4, name="Qux", description="A qux item", price=6.0, tax=0.5),
    Item(id=5, name="Quux", description="A quux item", price=4.0, tax=0.5),
]


@app.get("/")
async def root():
    return {"message": "Hello World asdfasdf asdf"}


@app.get("/items/", response_model=list[Item])
async def read_items(
    q: str | None = None, skip: int = 0, limit: int = 10
) -> list[Item]:
    if q:
        return [item for item in fake_items_db if q in item.name]
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int) -> Item:
    for item in fake_items_db:
        if item.id == item_id:
            return item

    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: CreateItem) -> Item:
    new_id = max(i.id for i in fake_items_db) + 1
    new_item = Item(id=new_id, **item.model_dump())
    fake_items_db.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: UpdateItem) -> Item:
    for existing in fake_items_db:
        if existing.id == item_id:
            data = item.model_dump(exclude_unset=True)
            for field, value in data.items():
                setattr(existing, field, value)
            return existing

    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int) -> None:
    for i, item in enumerate(fake_items_db):
        if item.id == item_id:
            fake_items_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run(
        "fastapi_tutorial.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir="src",
    )
