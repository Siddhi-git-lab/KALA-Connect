from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.product import Product, BuyerInquiry
from app.schemas.product import (
    ProductResponse, 
    BuyerInquiryCreate, 
    BuyerInquiryResponse
)

router = APIRouter(prefix="/api/marketplace", tags=["Marketplace & Buyer Matching"])

@router.get("/products", response_model=List[ProductResponse])
def get_marketplace_products(
    category: Optional[str] = Query(None, description="Filter by craft category"),
    search: Optional[str] = Query(None, description="Search keyword in title"),
    db: Session = Depends(get_db)
):
    """Filter and match products for buyers based on category or search terms."""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
        
    if search:
        query = query.filter(Product.title.ilike(f"%{search}%"))
        
    return query.all()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_details(product_id: int, db: Session = Depends(get_db)):
    """Fetch details of a specific artisan product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products/{product_id}/inquiries", response_model=BuyerInquiryResponse)
def create_buyer_inquiry(
    product_id: int,
    inquiry: BuyerInquiryCreate,
    db: Session = Depends(get_db)
):
    """Establish market linkage by sending an inquiry to the product's artisan."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    new_inquiry = BuyerInquiry(
        product_id=product_id,
        buyer_name=inquiry.buyer_name,
        buyer_email=inquiry.buyer_email,
        message=inquiry.message
    )
    
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry