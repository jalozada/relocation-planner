# Codex Instructions

## Development Approach

- Work on one clearly defined feature at a time.
- Stop after completing the requested milestone.
- Do not add unrequested features.
- Do not add a dependency without explaining why it is necessary.
- Prefer Django built-in capabilities over additional packages.
- Keep the application local-first and SQLite-compatible.
- Keep business rules separate from templates and views.
- Never hard-code Javier, Ursula, Antonella, Argentina, American Airlines,
  baggage fees, or currencies into application logic.
- Add validation and tests for calculations.
- Preserve all existing working behavior.
- Keep templates usable on desktop and mobile browsers.
- Do not store passport scans, Social Security numbers, medical records,
  or other highly sensitive documents.
- Update documentation when behavior or architecture changes.

## Validation Standard

Each milestone must include:

1. Application starts successfully.
2. Database migrations succeed.
3. Automated tests pass.
4. The requested behavior works through the user interface.
5. No unrelated feature changes are included.
