F-001 — Broken Object Level Authorization (BOLA)
- Threat category: STRIDE — Information Disclosure.
- Affected endpoint: GET /claims/{claim_id}.
- Root cause: Missing object-level authorization.
- Expected behavior: HTTP 403 para una solicitud autenticada de Alice sobre el expediente de Bob.
- Observed behavior: HTTP 200 con los datos de Bob.
- Remediation: Implementar autenticación y verificar la titularidad del expediente.