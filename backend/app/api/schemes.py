from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/schemes", tags=["Scheme Guidance"])

GOVT_SCHEMES = [
    {
        "scheme_id": "SCH01",
        "scheme_name": "PM Vishwakarma Yojana",
        "category_focus": ["Terracotta", "Woodwork", "Brassware", "Handloom", "Pottery", "All"],
        "max_loan_subsidy": "₹3,00,000 at 5% interest",
        "benefits": "Skill training (₹500/day stipend), ₹15,000 modern toolkit incentive, credit support & brand marketing.",
        "eligibility": "Rural and urban traditional artisans and craftspersons working with hands and tools.",
        "portal_url": "https://pmvishwakarma.gov.in"
    },
    {
        "scheme_id": "SCH02",
        "scheme_name": "One District One Product (ODOP)",
        "category_focus": ["Handloom", "Silk", "Woodwork", "Brassware", "Pottery", "Textiles"],
        "max_loan_subsidy": "Up to ₹5,00,000 market & exhibition grants",
        "benefits": "Geographic branding, export promotion, onboarding to Government e-Marketplace (GeM) & ONDC.",
        "eligibility": "Artisans producing indigenous district-specific crafts.",
        "portal_url": "https://odop.esuvidha.gov.in"
    },
    {
        "scheme_id": "SCH03",
        "scheme_name": "Ambedkar Hastshilp Vikas Yojana (AHVY)",
        "category_focus": ["Terracotta", "Handicrafts", "Tribal Art", "All"],
        "max_loan_subsidy": "Cluster infrastructure grant up to ₹10,00,000",
        "benefits": "Self-help group mobilization, design innovation workshops, buyer-seller direct meets.",
        "eligibility": "Empaneled handicraft artisans and Self Help Groups (SHGs).",
        "portal_url": "https://handicrafts.nic.in"
    },
    {
        "scheme_id": "SCH04",
        "scheme_name": "Pradhan Mantri Mudra Yojana (Shishu / Kishor)",
        "category_focus": ["All"],
        "max_loan_subsidy": "Collateral-free loans from ₹50,000 to ₹5,00,000",
        "benefits": "Working capital to buy raw materials (threads, clay, wood, dyes) and craft machinery.",
        "eligibility": "Micro-enterprises, rural weavers, and unorganized artisans.",
        "portal_url": "https://www.mudra.org.in"
    }
]

class SchemeFilterRequest(BaseModel):
    category: str
    annual_turnover: Optional[float] = 0.0

@router.post("/recommend")
def recommend_schemes(payload: SchemeFilterRequest):
    craft = payload.category.strip().title()

    # Prioritize schemes matching craft category directly, followed by universal craft schemes
    primary_matches = [s for s in GOVT_SCHEMES if craft in s["category_focus"]]
    fallback_matches = [s for s in GOVT_SCHEMES if "All" in s["category_focus"] and s not in primary_matches]

    recommended = primary_matches + fallback_matches
    return {
        "artisan_category": craft,
        "count": len(recommended),
        "schemes": recommended
    }