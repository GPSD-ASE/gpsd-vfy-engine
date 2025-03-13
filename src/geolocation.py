from fastapi import HTTPException
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

from src.models import Coordinates, AddressResponse
from src.utils.logger import get_logger

load_dotenv()

class GeoLocationService:
    def __init__(self):
        self.logger = get_logger("geolocation_service")
        self.api_key = os.getenv("GEOCODING_API_KEY")

        if not self.api_key:
            self.logger.warning("No GEOCODING_API_KEY found in environment variables!")

        # default to Nominatim (OpenStreetMap) if no API key is provided
        self.service_url = "https://nominatim.openstreetmap.org/reverse"

        # if self.api_key:
        #     self.service_url = "https://maps.googleapis.com/maps/api/geocode/json"

    async def reverse_geocode(self, coordinates: Coordinates) -> AddressResponse:
        """
        Convert coordinates to an address using an external geocoding service

        Args:
            coordinates: Coordinates model with latitude and longitude

        Returns:
            AddressResponse with the resolved address

        Raises:
            HTTPException: For various error conditions
        """
        try:
            params = {
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "format": "json",
                "addressdetails": 1,
            }

            headers = {
                "User-Agent": "GPSDApp/1.0"  # Required by Nominatim
            }
            # if self.api_key:
            #    params = {
            #        "latlng": f"{coordinates.latitude},{coordinates.longitude}",
            #        "key": self.api_key
            #    }

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.service_url,
                    params=params,
                    headers=headers
                )

                response.raise_for_status()
                result = response.json()

                if "error" in result:
                    self.logger.error(f"Error from geocoding provider: {result['error']}")
                    raise HTTPException(status_code=400, detail=result["error"])

                # extract address from response (format depends on provider) for Nominatim:
                address = result.get("display_name", "Address not found")

                # if result.get("status") == "OK" and result.get("results"):
                #     address = result["results"][0].get("formatted_address", "Address not found")
                # else:
                #     address = "Address not found"

                return AddressResponse(
                    address=address,
                    full_response=result,
                    coordinates=coordinates
                )

        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error during geocoding request: {e}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

        except httpx.RequestError as e:
            self.logger.error(f"Request error during geocoding request: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable")

        except Exception as e:
            self.logger.error(f"Unexpected error during geocoding: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
