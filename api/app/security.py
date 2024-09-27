import os
import secrets
import bcrypt
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import APIKey
from .models import APIKey
from .database import get_db

def get_api_key(api_key: str = Header(...), db: Session = Depends(get_db)):
    stored_key = db.query(APIKey).filter(APIKey.is_active == True).first()

    # Check if the API key has expired
    if not stored_key or stored_key.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="API Key has expired")

    if not bcrypt.checkpw(api_key.encode(), stored_key.key.encode()):
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # Update last used time
    stored_key.last_used_at = datetime.utcnow()
    db.commit()

    return api_key




def create_api_key(db: Session):
    # Generate a random API key
    raw_key = secrets.token_urlsafe(32)
    hashed_key = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt()).decode()

    # Store the hashed key in the database
    api_key = APIKey(key=hashed_key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return raw_key
