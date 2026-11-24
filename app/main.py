
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
        "owner_sub": "1943016f-f1d0-4534-8981-555b8686a81f",
        "customer": "Alice",
        "claim_amount": 2500,
        "status": "approved"
    },
    1002: {
        "owner_sub": "6c8a2ab5-b931-4c18-9f2b-97669aa9928a",
        "customer": "Bob",
        "claim_amount": 7500,
        "status": "pending"
    }
}


@app.get("/claims/{claim_id}")
def get_claim(
    claim_id: int,
    current_user: dict = Depends(get_current_user)
):
    if claim_id not in claims:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    claim = claims[claim_id]

    if claim["owner_sub"] != current_user["sub"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return {
        "customer": claim["customer"],
        "claim_amount": claim["claim_amount"],
        "status": claim["status"]
    }


@app.get("/me")
def read_current_user(
    current_user: dict = Depends(get_current_user)
):
    return {
        "subject": current_user["sub"],
        "username": current_user.get("preferred_username")
    }
