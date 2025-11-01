from fastapi import FastAPI
from app.schemas import WordResponse
from fastapi import HTTPException
 
from app.routers import words
 
# Initialize FastAPI app
app = FastAPI(
    title="Vocabulary Practice API",
    version="1.0.0",
    description="API for vocabulary practice and learning"
)
 
 
# Replace function get_random_word with route
app.include_router(words.router, prefix="/api", tags=["words"])
 
 
@app.get("/")
def read_root():
    return {
        "message": "Vocabulary Practice API",
        "version": "1.0.0",
        "endpoints": {
            "random_word": "/api/word",
            "validate": "/api/validate-sentence",
            "summary": "/api/summary",
            "history": "/api/history"
        }
    }