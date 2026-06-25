import os
from fastapi import Header, HTTPException


API_KEY = os.getenv("API_KEY")

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key