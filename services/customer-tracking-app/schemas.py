from pydantic import BaseModel

class TokenData(BaseModel):
    username: str

class Product(BaseModel):
    product_id: int
    slug: str
    category_id: int
    ratings: float
    original_price: float
    stock: int