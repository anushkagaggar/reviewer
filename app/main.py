from fastapi import FastAPI
from app.api.review import router as review_router

app = FastAPI(title="AI Design Reviewer")

app.include_router(review_router)

@app.get("/health")
def health():
    return {"status": "ok"}
