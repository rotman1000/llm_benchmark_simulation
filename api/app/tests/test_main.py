import os
import bcrypt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from main import app  # Your FastAPI app
from database import Base, get_db
from models import APIKey

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a TestClient for FastAPI
client = TestClient(app)

# Create and drop tables for tests
@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Helper function to generate hashed API key
def generate_api_key(db, raw_key, is_active=True, expires_at=None):
    hashed_key = bcrypt.hashpw(raw_key.encode(), bcrypt.gensalt()).decode()
    api_key = APIKey(
        key=hashed_key,
        is_active=is_active,
        expires_at=expires_at or (datetime.utcnow() + timedelta(days=30))
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    yield db
    db.close()

# Test creating a valid API key
def test_create_valid_api_key(test_db):
    raw_key = "test_valid_api_key"
    api_key = generate_api_key(test_db, raw_key)

    assert api_key is not None
    assert api_key.is_active is True
    assert bcrypt.checkpw(raw_key.encode(), api_key.key.encode()) is True

# Test valid API key request
def test_valid_api_key_access(test_db):
    raw_key = "test_valid_api_key_access"
    api_key = generate_api_key(test_db, raw_key)

    # Send request with valid API key
    response = client.get("/rankings/accuracy", headers={"api-key": raw_key})
    assert response.status_code != 403  # Ensure no forbidden response

# Test invalid API key request
def test_invalid_api_key_access(test_db):
    raw_key = "test_valid_api_key_access"
    invalid_key = "invalid_key"
    generate_api_key(test_db, raw_key)

    # Send request with invalid API key
    response = client.get("/rankings/accuracy", headers={"api-key": invalid_key})
    assert response.status_code == 403  # Should return forbidden
    assert response.json() == {"detail": "Invalid API Key"}

# Test expired API key request
def test_expired_api_key(test_db):
    raw_key = "test_expired_api_key"
    expired_time = datetime.utcnow() - timedelta(days=1)  # Expired yesterday
    generate_api_key(test_db, raw_key, expires_at=expired_time)

    # Send request with expired API key
    response = client.get("/rankings/accuracy", headers={"api-key": raw_key})
    assert response.status_code == 403  # Should return forbidden due to expiration
    assert response.json() == {"detail": "API Key has expired"}

# Test revoked API key request
def test_revoked_api_key(test_db):
    raw_key = "test_revoked_api_key"
    api_key = generate_api_key(test_db, raw_key, is_active=False)

    # Send request with revoked API key
    response = client.get("/rankings/accuracy", headers={"api-key": raw_key})
    assert response.status_code == 403  # Should return forbidden due to revocation
    assert response.json() == {"detail": "Invalid API Key"}

# Test revoking API key
def test_revoke_api_key(test_db):
    raw_key = "test_to_revoke_api_key"
    api_key = generate_api_key(test_db, raw_key)

    # Revoke the API key
    response = client.post(f"/api-keys/revoke/{api_key.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "API Key revoked"}

    # Check that the API key is revoked
    response = client.get("/rankings/accuracy", headers={"api-key": raw_key})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API Key"}
