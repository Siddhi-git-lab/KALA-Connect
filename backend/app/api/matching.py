from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(prefix="/market", tags=["Market Intelligence"])

BUYER_REQUESTS = [
    {
        "buyer_id": "B101",
        "buyer_name": "FabIndia Sourcing Desk",
        "requirement": "Authentic handloom silk dupattas, banarasi weaves, and handwoven cotton sarees with traditional borders.",
        "preferred_location": "Varanasi / Pan-India",
        "order_volume": "Bulk (100+ pcs)"
    },
    {
        "buyer_id": "B102",
        "buyer_name": "Dastkar Crafts Collective",
        "requirement": "Eco-friendly terracotta pottery, clay earthen cookware, and handmade decorative kulhads.",
        "preferred_location": "Uttar Pradesh / Rajasthan",
        "order_volume": "Medium (50-200 pcs)"
    },
    {
        "buyer_id": "B103",
        "buyer_name": "LivingSpaces Decor Studio",
        "requirement": "Hand-carved wooden sculptures, wooden wall panels, and brass inlaid handicraft furniture.",
        "preferred_location": "Saharanpur / Pan-India",
        "order_volume": "Custom / Retail"
    },
    {
        "buyer_id": "B104",
        "buyer_name": "Tribal Heritage Store",
        "requirement": "Handcrafted tribal jewelry, brass Dhokra art, and natural organic dye paintings.",
        "preferred_location": "Bastar / Odisha",
        "order_volume": "Batch (30-100 pcs)"
    }
]

class ProductMatchRequest(BaseModel):
    title: str
    category: str
    material: str
    tags: List[str]

@router.post("/match-buyers")
def match_buyers_for_product(payload: ProductMatchRequest):
    # Construct combined search query from artisan input
    product_query = f"{payload.title} {payload.category} {payload.material} {' '.join(payload.tags)}"
    buyer_texts = [b["requirement"] for b in BUYER_REQUESTS]

    # Calculate TF-IDF Cosine Similarity across corpus
    corpus = [product_query] + buyer_texts
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()

    # Compare product (index 0) against all buyers (indices 1..)
    product_vector = [vectors[0]]
    buyer_vectors = vectors[1:]
    scores = cosine_similarity(product_vector, buyer_vectors)[0]

    results = []
    for idx, score in enumerate(scores):
        # Scale score for UI display (with baseline relevance)
        scaled_score = round(max(float(score) * 100, 45.0 + float(score) * 50), 1)
        results.append({
            "buyer_id": BUYER_REQUESTS[idx]["buyer_id"],
            "buyer_name": BUYER_REQUESTS[idx]["buyer_name"],
            "requirement": BUYER_REQUESTS[idx]["requirement"],
            "preferred_location": BUYER_REQUESTS[idx]["preferred_location"],
            "order_volume": BUYER_REQUESTS[idx]["order_volume"],
            "match_score": scaled_score
        })

    # Rank by best match
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)
    return {"matched_buyers": results}