import os
import secrets
from fastapi import Header, HTTPException


API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str = Header(...)):
    if not secrets.compare_digest(api_key, API_KEY or ""):
        raise HTTPException(
            status_code=401, 
            detail="Invalid API Key"
        )
    return api_key