from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Artisan AI & Market Linkage Engine")

# Allow requests from the Flutter app and Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
model = joblib.load('pricing_model.pkl')

class PricingRequest(BaseModel):
    category: str
    material_cost: float
    labor_hours: float
    craft_complexity: int

@app.post("/predict-price")
def predict_price(item: PricingRequest):
    input_df = pd.DataFrame([item.model_dump()])
    fair_price = float(model.predict(input_df)[0])
    floor_price = item.material_cost + (item.labor_hours * 70)
    
    return {
        "status": "success",
        "recommended_price": round(fair_price, 2),
        "minimum_floor_price": round(floor_price, 2),
        "suggested_festival_price": round(fair_price * 1.20, 2),
        "currency": "INR"
    }

@app.get("/market-trends")
def market_trends():
    return {
        "trending_categories": ["Terracotta", "Madhubani"],
        "high_demand_region": "North India",
        "average_margin": "28%"
    }
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# In-memory artisan catalog for demonstration
ARTISAN_PRODUCTS = [
    {"id": 1, "name": "Terracotta Tea Cups", "category": "Terracotta", "tags": "clay terracotta tea cup kulhad handmade earthenware red", "artisan": "Ramesh Kumar"},
    {"id": 2, "name": "Madhubani Fish Wall Art", "category": "Madhubani", "tags": "madhubani painting folk fish canvas traditional handmade mithila", "artisan": "Sita Devi"},
    {"id": 3, "name": "Handloom Zari Saree", "category": "Zari Work", "tags": "silk zari embroidery wedding handloom traditional banarasi", "artisan": "Anjali Bai"},
    {"id": 4, "name": "Carved Wooden Elephant", "category": "Woodcraft", "tags": "wooden elephant carving decorative saharanpur walnut teak", "artisan": "Mohammad Arif"}
]

class BuyerQuery(BaseModel):
    query: str

@app.post("/match-buyer")
def match_buyer(buyer: BuyerQuery):
    product_descriptions = [p["tags"] for p in ARTISAN_PRODUCTS]
    corpus = [buyer.query] + product_descriptions
    
    # Calculate similarity scores
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    query_vector = vectors[0].reshape(1, -1)
    product_vectors = vectors[1:]
    
    similarities = cosine_similarity(query_vector, product_vectors)[0]
    
    # Rank by best match
    ranked_indices = similarities.argsort()[::-1]
    
    matches = []
    for idx in ranked_indices:
        if similarities[idx] > 0.05:
            match_data = dict(ARTISAN_PRODUCTS[idx])
            match_data["match_score"] = round(float(similarities[idx]) * 100, 1)
            matches.append(match_data)
            
    return {
        "status": "success",
        "total_matches": len(matches),
        "results": matches if matches else "No close matches found. Try different keywords."
    }
