from pydantic import BaseModel
from typing import Optional

class InsertPointRequestBody(BaseModel):
    slug: str
    product_id: int
    product_name: str
    
class UpdatePointRequestBody(BaseModel):
    slug: Optional[str] = None
    product_id: int
    product_name: Optional[str] = None
    
class SearchQueryParams(BaseModel):
    slug: str  
    limit: int = 10  # Optional, with default value
    thresh: float = 0.0  # Optional, with default value