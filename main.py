"""
main.py
"""
import uvicorn

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from src.models import Coordinates, AddressResponse
from src.geolocation import GeoLocationService
from src.utils.logger import get_logger


logger = get_logger("main")

app = FastAPI(
    title="GPSD Reverse Geolocation Service",
    description="GPSD Microservice to convert GPS coordinates to street addresses",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, we can replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

geo_service = GeoLocationService()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}

@app.post("/api/v1/geolocation/reverse", response_model=AddressResponse)
async def reverse_geocode(coordinates: Coordinates):
    """
    Convert GPS coordinates to a street address using a geocoding service.
    """
    try:
        logger.info(f"Processing reverse geocoding request for coordinates: {coordinates}")
        result = await geo_service.reverse_geocode(coordinates)
        return result

    except Exception as e:
        logger.error(f"Error in reverse geocode endpoint: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9500)
