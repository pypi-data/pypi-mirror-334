"""API client for HostSpace services."""
from typing import Optional, Dict, Any
import requests
from requests.exceptions import RequestException

from hostspace.utils.config import config

class APIClient:
    def __init__(self):
        self.base_url = config.get_endpoint()
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Configure the requests session with default headers and auth."""
        api_key = config.get_api_key()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and errors."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return {"message": response.text}
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise APIError("Authentication failed. Please check your API key.")
            elif response.status_code == 403:
                raise APIError("Permission denied. Please check your access rights.")
            elif response.status_code == 404:
                raise APIError("Resource not found.")
            else:
                raise APIError(f"HTTP Error: {str(e)}")
        except RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send GET request to API."""
        response = self.session.get(f"{self.base_url}{path}", params=params)
        return self._handle_response(response)

    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send POST request to API."""
        response = self.session.post(f"{self.base_url}{path}", json=data)
        return self._handle_response(response)

    def put(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send PUT request to API."""
        response = self.session.put(f"{self.base_url}{path}", json=data)
        return self._handle_response(response)

    def delete(self, path: str) -> Dict[str, Any]:
        """Send DELETE request to API."""
        response = self.session.delete(f"{self.base_url}{path}")
        return self._handle_response(response)

class APIError(Exception):
    """Custom exception for API errors."""
    pass

api_client = APIClient()
