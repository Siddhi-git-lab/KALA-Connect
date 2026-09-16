import os
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

try:
    import joblib
    import pandas as pd
    pricing_model = joblib.load("pricing_model.pkl")
except Exception:
    pricing_model = None

router = APIRouter()
client = genai.Client()

class CatalogResponse(BaseModel):
    title: str = Field(description="Market-ready title for the artisan craft")
    category: str = Field(description="Handicraft category, e.g., Terracotta, Handloom, Brassware, Woodwork")
    material: str = Field(description="Primary materials used, e.g., Clay, Silk, Rosewood, Brass")
    tags: List[str] = Field(description="5 to 7 search tags for digital buyer discovery")
    description_en: str = Field(description="Compelling, story-driven e-commerce product description in English")
    description_hi: str = Field(description="Accurate Hindi translation of the description for local artisans")
    suggested_price: float = Field(description="Estimated fair selling price in INR")

def estimate_price(category: str, material: str) -> float:
    if pricing_model is not None:
        try:
            df = pd.DataFrame([{"category": category, "material": material, "labor_hours": 6.0}])
            return round(float(pricing_model.predict(df)[0]), 2)
        except Exception:
            pass
    fallback_map = {"Handloom": 1200.0, "Terracotta": 450.0, "Woodwork": 1500.0, "Brassware": 2200.0}
    return fallback_map.get(category, 650.0)

@router.post("/auto-generate", response_model=CatalogResponse)
async def auto_generate_catalog(
    file: UploadFile = File(...),
    artisan_notes: Optional[str] = Form(default="")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image (.jpg, .png, .jpeg)")
    
    image_bytes = await file.read()

    prompt = f"""
    You are an AI assistant for rural and marginalized Indian artisans.
    Analyze the uploaded handicraft product photo.
    Additional artisan notes: "{artisan_notes}".

    Extract:
    1. A culturally authentic, attractive e-commerce product title.
    2. Primary handicraft category.
    3. Material composition.
    4. 5 to 7 high-intent search tags for digital buyer discovery.
    5. A compelling description in both English and Hindi.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=file.content_type),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CatalogResponse,
                temperature=0.2
            )
        )
        catalog = response.parsed
        catalog.suggested_price = estimate_price(catalog.category, catalog.material)
        return catalog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Catalog generation failed: {str(e)}")