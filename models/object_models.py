from pydantic import BaseModel


class ItemData(BaseModel):
    createdAt: str
    name: str
    price: int
    sellerId: int
    statistics: dict[str, int]

class StatsData(BaseModel):
    contacts: int
    likes: int
    viewCount: int

class NullItemData(BaseModel):
    result: dict
    status: str
class CreateItemData(BaseModel):
    status: str