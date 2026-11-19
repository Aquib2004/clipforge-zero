# Security Policy

## Reporting a Vulnerability

Email the maintainers at `security@clipforge-zero.local` (placeholder — update
before public release) or open a **private** GitHub Security Advisory. Please do
not open public issues for security bugs. Include: affected version, repro steps,
and impact assessment.

We respond within 72 hours with an acknowledgement and a remediation plan.

## Threat model

ClipForge Zero is a **local-first, single-user** tool.

- The backend binds to `127.0.0.1` by default. Non-loopback binding is not supported in Phase 1.
- Secrets (Gemini/Groq API keys, OAuth tokens) are held in the OS keychain via the `keyring` package; the frontend never sees raw secret values.
- API responses never return secret values.
- All subprocess calls use `shell=False` with argument lists.
- A workspace path guard prevents path traversal and writes outside `data/`.
- Structured logging redacts API keys, tokens, and authorization headers.
- No telemetry, no analytics, no hidden network requests.

## Supported versions

Only the latest commit on `main` is supported during pre-1.0 development.

## What is NOT yet implemented (Phase 1)

- OS-native credential storage integration (planned for Phase 4)
- Rate limiting (planned for a later phase)
- CSRF protections (planned for a later phase)
