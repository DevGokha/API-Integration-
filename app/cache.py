# app/cache.py
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from .api_client import fetch_posts, fetch_users, ExternalAPIError

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

POSTS_CACHE_FILE = CACHE_DIR / "posts.json"
USERS_CACHE_FILE = CACHE_DIR / "users.json"

_memory_cache = {
    "posts": None,
    "users": None,
}

def _load_from_file(path: Path) -> Optional[List[Dict[str, Any]]]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except Exception:
        return None
    return None

def _save_to_file(path: Path, data: List[Dict[str, Any]]) -> None:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        # For this assignment, we silently ignore file write errors
        pass

def get_posts(force_refresh: bool = False) -> List[Dict[str, Any]]:
    if not force_refresh and _memory_cache["posts"] is not None:
        return _memory_cache["posts"]

    data = _load_from_file(POSTS_CACHE_FILE) if not force_refresh else None
    if data is None:
        # Fetch from API
        data = fetch_posts()
        _save_to_file(POSTS_CACHE_FILE, data)

    _memory_cache["posts"] = data
    return data

def get_users(force_refresh: bool = False) -> List[Dict[str, Any]]:
    if not force_refresh and _memory_cache["users"] is not None:
        return _memory_cache["users"]

    data = _load_from_file(USERS_CACHE_FILE) if not force_refresh else None
    if data is None:
        data = fetch_users()
        _save_to_file(USERS_CACHE_FILE, data)

    _memory_cache["users"] = data
    return data
