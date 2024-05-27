from pydantic import BaseModel
from typing import Optional

class InsertPointRequestBody(BaseModel):
    slug: str
    product_id: str
    product_name: str
    product_image_url: str
    
class UpdatePointRequestBody(BaseModel):
    slug: Optional[str] = None
    product_id: int
    product_name: Optional[str] = None
    product_image_url: Optional[str] = None