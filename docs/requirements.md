# Security and Functional Requirements

## 1. Purpose

This document defines the functional and security requirements for the STRIDE Threat Modeling & Security Validation Lab.

The laboratory uses a FastAPI-based insurance Claims API to demonstrate how security threats can be identified, translated into defensive requirements, and validated through automated testing.

## 2. Scope

The laboratory focuses on:

- API security requirements.
- STRIDE threat identification.
- Object-level authorization.
- Broken Object Level Authorization (BOLA) testing.
- Security control validation.
- Automated testing using pytest.
- Security evidence collection.

The application uses fictional insurance claims and runs in a local development environment.

## 3. Functional Requirements

| ID | Requirement | Status |
|---|---|---|
| FR-01 | The API shall expose an application health endpoint. | Implemented |
| FR-02 | The API shall retrieve claims using a unique claim identifier. | Implemented |
| FR-03 | The application shall maintain fictional claims associated with individual customers. | Implemented |
| FR-04 | The API shall accept a simulated user identifier for laboratory testing. | Implemented |
| FR-05 | The API shall return HTTP 404 for nonexistent claims. | Implemented |

## 4. Security Requirements

### 4.1 Authentication and Identity

**SR-01 — Identity Verification**

The application shall verify the identity of a requesting user before allowing access to protected resources.

**STRIDE Category:** Spoofing

**Status:** Not implemented.

The current user query parameter is used solely for laboratory simulation and does not constitute authentication.

### 4.2 Object-Level Authorization

**SR-02 — Claim Ownership Validation**

The application shall verify that the authenticated user is authorized to access the requested insurance claim.

**STRIDE Categories:** Information Disclosure, Elevation of Privilege

**Status:** Not implemented.

**Acceptance Criteria:**

- A user can retrieve their own claim.
- A user cannot retrieve another user's claim.
- Unauthorized access attempts return HTTP 403 Forbidden.
- Automated tests verify both authorized and unauthorized access.

### 4.3 Input Validation

**SR-03 — Request Validation**

The application shall validate request parameters and reject invalid input.

**STRIDE Category:** Tampering

**Status:** Partially implemented through FastAPI request type validation.

**Acceptance Criteria:**

- Invalid claim identifiers are rejected.
- Malformed input does not cause unexpected application failures.
- Request validation errors produce appropriate HTTP responses.

### 4.4 Audit Logging

**SR-04 — Security Event Logging**

The application should record security-relevant access events.

**STRIDE Category:** Repudiation

**Status:** Not implemented.

**Acceptance Criteria:**

- Authorized claim access is recorded.
- Unauthorized access attempts are recorded.
- Logs include relevant timestamps and request context.
- Sensitive claim information is not unnecessarily exposed in logs.

### 4.5 Availability Protection

**SR-05 — API Availability**

The application should implement controls to reduce exposure to excessive or abusive requests.

**STRIDE Category:** Denial of Service

**Status:** Not implemented.

**Potential Controls:**

- Rate limiting.
- Request timeouts.
- Resource consumption monitoring.
- Error handling.

### 4.6 Least Privilege

**SR-06 — Access Restriction**

The application shall restrict access to resources according to the requesting user's authorized permissions.

**STRIDE Category:** Elevation of Privilege

**Status:** Not implemented.

**Acceptance Criteria:**

- Users can access only authorized claims.
- Unauthorized requests are denied.
- Access restrictions are enforced by the server.

## 5. Security Test Requirements

| Test ID | Test Scenario | Expected Result |
|---|---|---|
| ST-01 | Alice requests Alice's claim | HTTP 200 |
| ST-02 | Bob requests Bob's claim | HTTP 200 |
| ST-03 | Alice requests Bob's claim | HTTP 403 |
| ST-04 | Bob requests Alice's claim | HTTP 403 |
| ST-05 | User requests nonexistent claim | HTTP 404 |
| ST-06 | User supplies invalid claim identifier | HTTP 422 |

These are target outcomes for the remediated API. They do not imply that the current implementation passes every test.

## 6. Non-Functional Requirements

### NFR-01 — Testability

Security requirements shall be verifiable through repeatable automated tests.

### NFR-02 — Maintainability

Application code and automated tests should remain separate and clearly documented.

### NFR-03 — Reproducibility

The laboratory should be executable in a local Python environment using documented dependencies.

### NFR-04 — Evidence

Security test results should be retained as evidence of observed behavior and control effectiveness.

### NFR-05 — Data Protection

The laboratory shall use fictional customer information and avoid exposing real personal or confidential data.

## 7. Requirements Traceability

| Requirement | STRIDE Category | Validation |
|---|---|---|
| SR-01 | Spoofing | Authentication testing — future |
| SR-02 | Information Disclosure / Elevation of Privilege | Object-level authorization tests |
| SR-03 | Tampering | Input validation tests |
| SR-04 | Repudiation | Audit log verification — future |
| SR-05 | Denial of Service | Availability testing — future |
| SR-06 | Elevation of Privilege | Unauthorized access tests |

## 8. Limitations

The laboratory currently uses simulated user identities rather than an authentication provider.

The following capabilities are outside the current implementation:

- Production authentication and identity management.
- OAuth 2.0 / OpenID Connect integration.
- Persistent database storage.
- Enterprise audit logging.
- Production-grade rate limiting.
- Comprehensive API security testing.

These capabilities may be considered in future iterations.

## 9. Future Improvements

Potential enhancements include:

1. Implement claim ownership validation.
2. Complete positive and negative authorization tests.
3. Introduce authenticated identities using JWT or OpenID Connect.
4. Add structured security audit logging.
5. Extend automated security testing.
6. Map findings to OWASP API Security Top 10.
7. Document residual risks and architectural decisions.