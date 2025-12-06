  # app/main.py
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

from .schemas import Post, User, ErrorResponse
from .cache import get_posts, get_users
from .api_client import ExternalAPIError

app = FastAPI(
    title="JSONPlaceholder API Integration Demo",
    description="Mini application for GLOBAL TREND internship assignment.",
    version="1.0.0",
)

@app.get("/posts", response_model=List[Post], responses={502: {"model": ErrorResponse}})
def list_posts(
    user_id: Optional[int] = Query(None, alias="userId", description="Filter by userId"),
    title_contains: Optional[str] = Query(None, description="Filter by keyword in title"),
    refresh: bool = Query(False, description="Force refresh cache from upstream API"),
):
    """
    List posts with optional filters:
    - userId: filter posts by userId
    - title_contains: case-insensitive substring match in title
    - refresh: force refresh cache from upstream
    """
    try:
        posts_data = get_posts(force_refresh=refresh)
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

    # Basic filtering
    filtered = posts_data
    if user_id is not None:
        filtered = [p for p in filtered if p.get("userId") == user_id]

    if title_contains:
        t = title_contains.lower()
        filtered = [p for p in filtered if t in str(p.get("title", "")).lower()]

    # Pydantic will validate/mask malformed fields
    return filtered

@app.get("/posts/{post_id}", response_model=Post, responses={404: {"model": ErrorResponse}, 502: {"model": ErrorResponse}})
def get_post_detail(post_id: int, refresh: bool = Query(False)):
    """
    Get detailed view of a single post by its ID.
    """
    try:
        posts_data = get_posts(force_refresh=refresh)
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

    for p in posts_data:
        if p.get("id") == post_id:
            return p

    raise HTTPException(status_code=404, detail=f"Post with id={post_id} not found")

@app.get("/users", response_model=List[User], responses={502: {"model": ErrorResponse}})
def list_users(refresh: bool = Query(False)):
    """
    List all users (second upstream endpoint).
    """
    try:
        users_data = get_users(force_refresh=refresh)
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return users_data

@app.get("/users/{user_id}", response_model=User, responses={404: {"model": ErrorResponse}, 502: {"model": ErrorResponse}})
def get_user_detail(user_id: int, refresh: bool = Query(False)):
    """
    Get a single user by ID.
    """
    try:
        users_data = get_users(force_refresh=refresh)
    except ExternalAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))

    for u in users_data:
        if u.get("id") == user_id:
            return u

    raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
