# 04 — BOLA Security Regression Testing

## 1. Objective

Validate that the BOLA remediation prevents
unauthorized access to insurance claims while
preserving legitimate application functionality.

Regression testing must demonstrate that the
original vulnerability cannot be reproduced after
the security controls have been implemented.

## 2. Scope

The regression tests cover:

- JWT authentication.
- Object-level authorization.
- Horizontal privilege escalation.
- Unauthorized information disclosure.
- Legitimate access to insurance claims.
- Identity impersonation attempts.
- Application functionality after remediation.

## 3. Test Environment

| Component | Configuration |
|---|---|
| Application | Novaris Insurance API |
| Framework | FastAPI |
| Identity Provider | Keycloak |
| Realm | stride-lab |
| Audience | claims-api |
| Authentication | JWT Bearer token |
| Manual testing | Swagger UI / curl |
| Automated testing | pytest |
| Git branch | feature/bola-remediation |

## 4. Test Data

| Customer | Claim ID | Amount | Status |
|---|---|---|---|
| Alice | 1001 | 2500 | approved |
| Bob | 1002 | 7500 | pending |

Each customer must only be permitted to access
their own insurance claims.

## 5. Baseline Vulnerability Evidence

Before remediation, the API returned insurance
claim information without validating object
ownership.

| Requester | Claim | Expected | Baseline |
|---|---|---|---|
| Alice | 1001 | 200 | 200 |
| Alice | 1002 | 403 | 200 |
| Bob | 1002 | 200 | 200 |
| Bob | 1001 | 403 | 200 |

The baseline confirmed the existence of a
BOLA vulnerability.

See [TC-BOLA-001](TC-BOLA-001.md).

## 6. Regression Test Matrix

| Test ID | Scenario | Expected | Observed | Result |
|---|---|---|---|---|
| TC-BOLA-002 | Alice accesses claim 1001 | 200 | - | Pending |
| TC-BOLA-003 | Alice accesses claim 1002 | 403 | - | Pending |
| TC-BOLA-004 | Bob accesses claim 1002 | 200 | - | Pending |
| TC-BOLA-005 | Bob accesses claim 1001 | 403 | - | Pending |
| TC-BOLA-006 | Missing JWT | 401 | - | Pending |
| TC-BOLA-007 | Invalid JWT | 401 | - | Pending |
| TC-BOLA-008 | Nonexistent claim | 404 | - | Pending |
| TC-BOLA-009 | Identity override attempt | 403 | - | Pending |

TC-BOLA-009 will verify that supplying another
username cannot override the authenticated identity.

## 7. Positive and Negative Testing

### Positive Tests

Verify that authorized users retain access
to their legitimate resources.

- Alice can access claim 1001.
- Bob can access claim 1002.
- Authorized responses contain the expected data.

### Negative Tests

Verify that unauthorized requests are rejected.

- Alice cannot access Bob's claim.
- Bob cannot access Alice's claim.
- Requests without credentials are rejected.
- Requests with invalid credentials are rejected.
- User-supplied identity cannot override JWT identity.
- Denied responses do not disclose claim data.

## 8. Automated Regression Testing

The automated authorization tests are located in:

`tests/test_authorization.py`

The existing tests must be reviewed and updated
to reflect the remediated security architecture.

### Activate the virtual environment

```bash
source .venv/bin/activate
```

### Execute authorization tests

```bash
python -m pytest tests/test_authorization.py -v
```

### Execute the complete test suite

```bash
python -m pytest -v
```

### Automated Test Results

Status: Pending remediation implementation.

## 9. Manual Security Validation

Manual validation will be performed using:

- Swagger UI.
- curl.
- Valid Keycloak access tokens.
- Invalid access tokens.

Manual tests will complement automated tests
by validating integration with the actual
Identity Provider.

## 10. Security Control Traceability

| Threat | Control | Validation |
|---|---|---|
| Spoofing | JWT authentication | Authentication tests |
| Information Disclosure | Object ownership verification | BOLA regression tests |
| Elevation of Privilege | Object-level authorization | Cross-user access tests |
| Tampering | JWT signature verification | Invalid signature tests |

## 11. Acceptance Criteria

The BOLA remediation will be considered successful
when all applicable acceptance criteria are met.

- [ ] Alice can access her own claim.
- [ ] Bob can access his own claim.
- [ ] Alice cannot access Bob's claim.
- [ ] Bob cannot access Alice's claim.
- [ ] Missing tokens are rejected.
- [ ] Invalid tokens are rejected.
- [ ] Identity override attempts are unsuccessful.
- [ ] Unauthorized responses do not disclose claim data.
- [ ] Automated regression tests pass.
- [ ] Manual integration tests pass.
- [ ] Test evidence is documented.
- [ ] No regression in legitimate application functionality.

## 12. Evidence Collection

The following evidence will be collected:

- HTTP request and response results.
- Swagger UI screenshots.
- pytest execution output.
- Expected versus observed results.
- Git commit identifiers.
- Test execution dates.

Access tokens, passwords and private keys must
not be included in published test evidence.

## 13. Current Status

Status: TEST PLAN DEFINED

Date: 2026-11-24

The original BOLA vulnerability has been confirmed.

JWT authentication is undergoing validation.

Object-level authorization and post-remediation
regression testing remain pending.

## Related Documentation

- [BOLA Baseline Evidence](TC-BOLA-001.md)
- [Authorization Remediation](02-authorization-remediation.md)
- [JWT Authentication](../04-jwt-authentication.md)
- [Security Architecture](../architecture.md)