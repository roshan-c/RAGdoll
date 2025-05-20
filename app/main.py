from fastapi import FastAPI

from app.api import endpoints

app = FastAPI(
    title="Context Management Service",
    description="A service to manage and retrieve chat context using RAG and embeddings.",
    version="0.1.0"
)

# Placeholder root endpoint (optional, good for a basic health check)
@app.get("/")
async def root():
    return {"message": "Context Management Service is running"}

app.include_router(endpoints.router) 