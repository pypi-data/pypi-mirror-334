import httpx
import logging
from typing import Any, Dict
logging.basicConfig(level=logging.INFO, format="%(message)s")
class ApiService:
    """
    ApiService is a utility class for making HTTP POST requests to external APIs. Its static method,
    make_api_call, constructs the API endpoint URL and sends a POST request with provided data and headers,
    including an API key for authorization. It abstracts away HTTP request complexity, leveraging the requests
    library, and offers a centralized interface for API interaction within applications.
    """
    @staticmethod
    async def make_api_call(
        base_url: str,
        api_url: str,
        data: Dict[str, Any],
        api_key: str
    ) -> Dict[str, Any]:
        actual_url = base_url.rstrip("/") + "/" + api_url.lstrip("/")
        headers = {"x-api-key": api_key}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(actual_url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logging.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
                raise e