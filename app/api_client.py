# app/api_client.py
import requests
from typing import List, Dict, Any
from .config import BASE_URL, REQUEST_TIMEOUT

class ExternalAPIError(Exception):
    """Custom exception for upstream API errors."""

def fetch_posts() -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/posts"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()  # HTTP errors
        data = resp.json()
        if not isinstance(data, list):
            raise ExternalAPIError("Invalid response format for posts")
        return data
    except requests.exceptions.Timeout:
        raise ExternalAPIError("Upstream API timeout while fetching posts")
    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(f"Network error while fetching posts: {e}")
    except ValueError:
        # .json() failed
        raise ExternalAPIError("Malformed JSON response for posts")

def fetch_users() -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/users"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ExternalAPIError("Invalid response format for users")
        return data
    except requests.exceptions.Timeout:
        raise ExternalAPIError("Upstream API timeout while fetching users")
    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(f"Network error while fetching users: {e}")
    except ValueError:
        raise ExternalAPIError("Malformed JSON response for users")
