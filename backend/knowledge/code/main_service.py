"""
Main Service Entry Point

This service initializes the FastAPI application
and wires together all API routes including the AI module.
"""

from fastapi import FastAPI
from api.ai import router as ai_router

app = FastAPI(title="Sample Backend Service")

app.include_router(ai_router)


@app.get("/")
def root():
    return {"message": "Service is running"}
