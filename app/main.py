
from fastapi import FastAPI, Depends, HTTPException
from app.auth import get_current_user


# Create our API application

app = FastAPI(
    title="Novaris Insurance API",
    description="STRIDE Threat Modeling & Security Validation Lab",
    version="0.1.0",
    swagger_ui_init_oauth={
        "clientId": "claims-api",
        "usePkceWithAuthorizationCodeGrant": True
    }
)


# Define our first API endpoint
@app.get("/")
def home():
    return {
        "application": "Novaris Insurance",
        "status": "running",
        "message": "Welcome to the STRIDE Security Validation Lab"
    }


# Fictional insurance claims for security testing
claims = {
    1001: {
        "customer": "Alice",
        "claim_amount": 2500,
        "status": "approved"
    },
    1002: {
        "customer": "Bob",
        "claim_amount": 7500,
        "status": "pending"
    }
}


@app.get("/claims/{claim_id}")
def get_claim(claim_id: int, user: str):
    if claim_id not in claims:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claims[claim_id]


@app.get("/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return {
        "subject": current_user["sub"],
        "username": current_user.get("preferred_username")
    }
