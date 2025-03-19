from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class ConfigDict:
        from_attributes = True