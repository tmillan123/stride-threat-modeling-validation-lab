## If you want a more visual “pretty” layout

This one usually looks more elegant in GitHub because it places **STRIDE around the application**:

```md
## STRIDE Threat Model

```mermaid
flowchart LR
    S["Spoofing"]
    T["Tampering"]
    R["Repudiation"]
    I["Information Disclosure"]
    D["Denial of Service"]
    E["Elevation of Privilege"]

    APP["Claims Application<br/>FastAPI Validation Lab"]

    S --> APP
    T --> APP
    R --> APP
    I --> APP
    D --> APP
    E --> APP

    APP --> C1["Authentication"]
    APP --> C2["Authorization"]
    APP --> C3["Input Validation"]
    APP --> C4["Audit Logging"]
    APP --> C5["Data Protection"]

    ___