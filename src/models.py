from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any

class Coordinates(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")

    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

class AddressResponse(BaseModel):
    address: str
    full_response: Optional[Dict[str, Any]] = None
    coordinates: Coordinates
