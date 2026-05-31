from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from backend.strava import get_authorization_url, exchange_code_for_token

router = APIRouter()

@router.get("/auth/login")
def login():
    url = get_authorization_url()
    return RedirectResponse(url)

@router.get("/auth/callback")
def callback(code: str):
    tokens = exchange_code_for_token(code)
    access_token = tokens.get("access_token")
    athlete = tokens.get("athlete")
    return {
        "access_token": access_token,
        "athlete": athlete
    }