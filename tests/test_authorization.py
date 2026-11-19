
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_application_health():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_existing_claim():
    response = client.get("/claims/1001?user=Alice")

    assert response.status_code == 200
    assert response.json()["customer"] == "Alice"


def test_missing_claim():
    response = client.get("/claims/9999?user=Alice")

    assert response.status_code == 404


def test_bola_vulnerability_reproduced():
    """
    Demonstrates the current insecure behavior.

    This test passes when Alice can retrieve Bob's claim.
    It documents a vulnerability, not a security success.
    """
    response = client.get("/claims/1002?user=Alice")

    assert response.status_code == 200
    assert response.json()["customer"] == "Bob"
def test_cross_customer_access_must_be_denied():
    """
    Security requirement:
    Alice must not access Bob's insurance claim.
    """
    response = client.get("/claims/1002?user=Alice")

    assert response.status_code == 403