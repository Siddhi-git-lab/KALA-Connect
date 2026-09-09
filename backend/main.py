from fastapi import FastAPI

app = FastAPI(title="KALA-Connect API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "KALA-Connect API is live"}