from fastapi import APIRouter, Depends, HTTPException
from ..models import items as item_models
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

items_db = [] # In-memory database for example

@router.post("/", response_model=item_models.Item)
async def create_item(item: item_models.ItemCreate):
    item_id = len(items_db) + 1
    new_item = item_models.Item(**item.dict(), id=item_id)
    items_db.append(new_item)
    return new_item

@router.get("/{item_id}", response_model=item_models.Item)
async def read_item(item_id: int):
    try:
      return items_db[item_id-1]
    except IndexError:
      raise HTTPException(status_code=404, detail="Item not found")

@router.get("/", response_model=List[item_models.Item])
async def read_items():
    return items_db