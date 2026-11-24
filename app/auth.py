
import jwt

from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer


# Trusted Identity Provider configuration
ISSUER = "http://127.0.0.1:8080/realms/stride-lab"
AUDIENCE = "claims-api"

JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
AUTHORIZATION_URL = f"{ISSUER}/protocol/openid-connect/auth"
TOKEN_URL = f"{ISSUER}/protocol/openid-connect/token"


# Initialize the JWT signing key client
jwks_client = PyJWKClient(JWKS_URL)


# OAuth 2.0 Authorization Code Flow
security = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes={"openid": "OpenID Connect authentication"},
    auto_error=False
)


def get_current_user(
    token: str | None = Depends(security)
):
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "iss", "aud", "sub"]}
        )

        return payload

    except jwt.exceptions.PyJWKClientConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Identity provider unavailable"
        )

    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"}
        )
