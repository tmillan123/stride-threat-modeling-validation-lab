
## STRIDE Threat Modeling & Security Validation

This project applies the **STRIDE threat modeling framework** to a FastAPI-based Claims API, identifying potential security threats, mapping them to defensive controls, and validating selected security behaviors through automated tests.

### Threat Model Overview

```mermaid
flowchart TB
    APP["🔐 FastAPI Claims API"]

    subgraph STRIDE["STRIDE Threat Categories"]
        direction TB
        S["S — Spoofing<br/>Identity impersonation"]
        T["T — Tampering<br/>Unauthorized data modification"]
        R["R — Repudiation<br/>Untraceable actions"]
        I["I — Information Disclosure<br/>Unauthorized claims access"]
        D["D — Denial of Service<br/>Service disruption"]
        E["E — Elevation of Privilege<br/>Authorization bypass"]
    end

    APP --> S
    APP --> T
    APP --> R
    APP --> I
    APP --> D
    APP --> E

    S -.-> C1["Authentication controls"]
    T -.-> C2["Input validation and integrity"]
    R -.-> C3["Audit logging"]
    I -.-> C4["Object-level authorization"]
    D -.-> C5["Rate limiting and resilience"]
    E -.-> C6["Least privilege and access checks"]

    C4 --> TEST["🧪 Authorization Tests"]
    C6 --> TEST

    TEST --> RESULT["Security validation evidence"]

    classDef application fill:#183153,color:#ffffff,stroke:#183153,stroke-width:2px
    classDef threat fill:#fff0e6,color:#823b13,stroke:#e59a57
    classDef control fill:#eaf3ff,color:#153c70,stroke:#83afe3
    classDef validation fill:#e7f6ee,color:#17603a,stroke:#69bb8f

    class APP application
    class S,T,R,I,D,E threat
    class C1,C2,C3,C4,C5,C6 control
    class TEST,RESULT validation
```

### Security Validation Focus

The lab demonstrates how threat modeling can inform practical security validation.

**Implemented validation focus:**
- Object-level authorization testing.
- Testing access to claims belonging to another user.
- Evaluating whether unauthorized requests are rejected.

**Additional STRIDE control areas:**
- Authentication and identity verification.
- Input validation and data integrity.
- Audit logging and accountability.
- Availability and resilience.
- Privilege enforcement.

These additional areas represent security considerations and potential extensions; their inclusion in the threat model does not imply that all controls have been implemented or tested.

### Supporting Documentation

- [Threat Model](docs/threat-model.md)
- [Security Findings](docs/security-findings.md)
- [Authorization Tests](tests/test_authorization.py)
