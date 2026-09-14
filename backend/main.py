from fastapi import FastAPI
from app.core.config import settings
from app.api.router import api_router

app = FastAPI(title=settings.PROJECT_NAME)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)
@app.get("/")
def read_root():
    return {"status": "online", "message": f"{settings.PROJECT_NAME} API is live"}