# 04 — JWT Authentication

## Objective

Implement and validate JWT-based authentication for the
Novaris Insurance Claims API using Keycloak as the Identity
Provider.

This security control addresses the Spoofing threat
category of the STRIDE framework.

## Environment

- Identity Provider: Keycloak
- Realm: stride-lab
- Audience: claims-api
- Resource Server: FastAPI
- PyJWT: 2.15.1
- cryptography: 50.0.2
- Signing algorithm: RS256
- Git branch: feature/bola-remediation

## Implementation

The authentication logic is implemented in `app/auth.py`.

The API retrieves public signing keys from Keycloak's
JWKS endpoint and validates:

- Digital signature
- Token issuer (iss)
- Intended audience (aud)
- Expiration time (exp)
- Subject identifier (sub)

The `/me` endpoint was introduced in `app/main.py`
to validate authentication independently of
object-level authorization.

## JWKS Validation

The public signing keys were successfully retrieved
from Keycloak.

```bash
curl -s \
  http://127.0.0.1:8080/realms/stride-lab/protocol/openid-connect/certs \
  | python -m json.tool
```

Two RSA public keys were returned:

- RSA-OAEP: Encryption key
- RS256: Signing key

## Authentication Test Cases

### TC-AUTH-001 — Missing Access Token

**Objective:** Verify that unauthenticated requests
are rejected.

**Test command:**

```bash
curl -i http://127.0.0.1:8000/me
```

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Response body:**

```json
{"detail":"Authentication required"}
```

**Result:** PASS

**Test date:** 2026-11-24

### TC-AUTH-002 — Invalid Access Token

**Objective:** Verify that the API rejects a malformed or fabricated access token.

**Test command:**

```bash
curl -i http://127.0.0.1:8000/me \
  -H "Authorization: Bearer invalid-token"
```

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Response body:**

```json
{"detail":"Invalid or expired access token"}
```

**Result:** PASS

**Test date:** 2026-11-24

### TC-AUTH-003 — Valid Alice Access Token

**Objective:** Verify that the API accepts a valid
Keycloak access token and correctly identifies
the authenticated user.

**Authentication method:**

- OAuth 2.0 Authorization Code Flow
- PKCE (S256)
- OpenID Connect
- Keycloak realm: stride-lab
- Client ID: claims-api
- User: alice

**Test procedure:**

1. Open Swagger UI.
2. Click Authorize.
3. Select the openid scope.
4. Authenticate through Keycloak.
5. Execute GET /me.

**Expected result:** HTTP 200 OK.

**Observed result:** HTTP 200 OK.

**Response body:**

```json
{
  "subject": "1943016f-f1d0-4534-8981-555b8686a81f",
  "username": "alice"
}
```

**Result:** PASS

**Test date:** 2026-11-24

### TC-AUTH-004 — Valid Bob Access Token

**Objective:** Verify that the API accepts a valid
Keycloak access token for Bob and correctly
distinguishes his identity from Alice's.

**Authentication method:** OAuth 2.0 Authorization
Code Flow with PKCE.

**Endpoint:** GET /me

**Expected result:** HTTP 200 OK with Bob's identity.

**Observed result:** HTTP 200 OK.

**Response body:**

```json
{
  "subject": "6c8a2ab5-b931-4c18-9f2b-97669aa9928a",
  "username": "bob"
}
```

**Result:** PASS

**Test date:** 2026-11-24

### TC-AUTH-005 — Expired Access Token

**Objective:** Verify that an expired but correctly
signed JWT is rejected.

**Method:** Automated component test using a signed
JWT with an expiration timestamp in the past.

**Test function:** `test_expired_token`

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Result:** PASS

### TC-AUTH-006 — Invalid Digital Signature

**Objective:** Verify that a JWT signed with an
untrusted private key is rejected.

**Method:** Generate a JWT using a different RSA
private key from the trusted test signing key.

All other required JWT claims remain valid.

**Test function:** `test_invalid_signature`

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Result:** PASS

### TC-AUTH-007 — Incorrect Audience

**Objective:** Verify that a correctly signed JWT
intended for another application is rejected.

**Test audience:** `another-api`

**Expected audience:** `claims-api`

**Test function:** `test_incorrect_audience`

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Result:** PASS

### TC-AUTH-008 — Incorrect Issuer

**Objective:** Verify that a correctly signed JWT
containing an untrusted issuer is rejected.

**Test issuer:** `https://untrusted-issuer.example`

**Test function:** `test_incorrect_issuer`

**Expected result:** HTTP 401 Unauthorized.

**Observed result:** HTTP 401 Unauthorized.

**Result:** PASS

## Automated Authentication Testing

The automated tests are implemented in:

`tests/test_authentication.py`

Temporary RSA key pairs are generated during
test execution.

Pytest monkeypatching substitutes JWKS signing
key retrieval, allowing individual JWT validation
controls to be tested independently.

The actual application JWT validation logic
remains unchanged.

### Test Execution

```bash
python -m pytest tests/test_authentication.py -v
```

### Execution Evidence

```text
test_valid_token PASSED
test_expired_token PASSED
test_invalid_signature PASSED
test_incorrect_audience PASSED
test_incorrect_issuer PASSED

5 passed, 1 warning in 0.42s
```

**Test date:** 2026-11-24

### Test Limitations

These are isolated component tests rather than
end-to-end Keycloak integration tests.

Live Keycloak integration was validated separately
through the successful authentication of Alice
and Bob using Swagger UI.

A non-blocking Starlette dependency deprecation
warning was observed.

## Security Conclusion

All planned authentication test cases passed.

The application correctly accepts valid access
tokens and rejects missing, malformed, expired,
incorrectly signed or incorrectly scoped tokens
under the tested conditions.
### Session Management Observation

Logging out of Swagger UI does not automatically
terminate the Keycloak SSO session.

During testing, Alice's existing SSO session was
initially reused.

Switching the Keycloak user session to Bob and
obtaining a new access token resolved the issue.

### Security Conclusion

The API successfully distinguishes between two
authenticated identities using their unique JWT
subject identifiers.

The integration between Swagger UI, Keycloak
and FastAPI was successfully validated.

Independent negative tests for signature, issuer,
audience and expiration validation remain pending.


## Test Results Summary

| Test ID | Scenario | Expected | Observed | Result |
|---|---|---|---|---|
| TC-AUTH-001 | Missing token | 401 | 401 | PASS |
| TC-AUTH-002 | Invalid token | 401 | 401 | PASS |
| TC-AUTH-003 | Valid Alice token | 200 | 200 | PASS |
| TC-AUTH-004 | Valid Bob token | 200 | 200 | PASS |
| TC-AUTH-005 | Expired token | 401 | 401 | PASS |
| TC-AUTH-006 | Invalid signature | 401 | 401 | PASS |
| TC-AUTH-007 | Incorrect audience | 401 | 401 | PASS |
| TC-AUTH-008 | Incorrect issuer | 401 | 401 | PASS |

## Current Limitations

- HTTP is used for local lab development.
- Full JWT validation testing is pending.
- Object-level authorization is not yet implemented.
- The Claims endpoint remains vulnerable to BOLA.