from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    category: str
    image_url: Optional[str] = None

    class Config:
        orm_mode = True

class ProductDetailResponse(ProductResponse):
    description: str
    artisan_id: int

    class Config:
        orm_mode = True

class InquiryCreate(BaseModel):
    product_id: int
    buyer_name: str
    buyer_email: str
    message: str