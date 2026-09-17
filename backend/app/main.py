from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers
from app.api import auth, users, marketplace, health
# If you created a schemes router earlier, import it too:
# from app.api import schemes 

app = FastAPI(
    title="KALA-Connect API",
    description="Platform empowering artisans with government schemes and market linkage.",
    version="1.0.0"
)

# Enable CORS so frontend apps (like React or mobile) can connect smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(marketplace.router)
app.include_router(health.router)

# Uncomment if you have a schemes router:
# app.include_router(schemes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to KALA-Connect API! Explore /docs for documentation."}