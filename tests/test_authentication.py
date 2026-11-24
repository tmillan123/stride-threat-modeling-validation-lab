
import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.main import app
from app.auth import ISSUER, AUDIENCE, jwks_client


client = TestClient(app)


@pytest.fixture
def signing_key(monkeypatch):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    monkeypatch.setattr(
        jwks_client,
        "get_signing_key_from_jwt",
        lambda token: SimpleNamespace(
            key=private_key.public_key()
        )
    )

    return private_key


def create_token(private_key, **overrides):
    payload = {
        "sub": "test-user",
        "preferred_username": "test-user",
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": int(time.time()),
        "exp": int(time.time()) + 300
    }

    payload.update(overrides)

    return jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )


def request_identity(token):
    return client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )


# Positive control
def test_valid_token(signing_key):
    token = create_token(signing_key)
    assert request_identity(token).status_code == 200


# TC-AUTH-005
def test_expired_token(signing_key):
    token = create_token(
        signing_key,
        iat=int(time.time()) - 600,
        exp=int(time.time()) - 300
    )

    assert request_identity(token).status_code == 401


# TC-AUTH-006
def test_invalid_signature(signing_key):
    untrusted_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    token = create_token(untrusted_key)

    assert request_identity(token).status_code == 401


# TC-AUTH-007
def test_incorrect_audience(signing_key):
    token = create_token(
        signing_key,
        aud="another-api"
    )

    assert request_identity(token).status_code == 401


# TC-AUTH-008
def test_incorrect_issuer(signing_key):
    token = create_token(
        signing_key,
        iss="https://untrusted-issuer.example"
    )

    assert request_identity(token).status_code == 401
