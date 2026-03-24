# AI Assembly Assistant (A3) - Gemini CLI Mandates

This document serves as the primary guidance for Gemini CLI while working on the A3 project. These mandates take absolute precedence over general defaults.

## Project Vision
A3 is an AI Assembly Assistant designed to integrate local vision and inference with production-ready streaming and API services.

## Architectural Integrity
- **Local vs. Production:** Keep `local/` (research, models, vision) strictly separated from `production/` (APIs, streaming).
- **Shared Utilities:** Use `shared/` for common interfaces, data models, and utility functions to ensure consistency across the stack.
- **Modularity:** Design for high cohesion and low coupling. Each component in `local/` and `production/` should be testable in isolation.

## Technical Standards
- **Type Safety:** Use strict typing (TypeScript for JS/TS, Pydantic/Type Hints for Python).
- **Documentation:** Every new function or class must include clear docstrings/comments. Maintain the `docs/` folder as the project evolves.
- **Clean Code:** Prioritize readability and long-term maintainability over clever optimizations.
- **Asynchronous Patterns:** Use `async/await` for all I/O-bound operations (streaming, API calls).

## Workflow & Validation
- **Test-Driven:** Always look for existing tests or create new ones in the relevant directory. A task is not complete until its behavioral correctness is verified.
- **Safe Execution:** For bug fixes, reproduction scripts are mandatory before applying a fix.
- **Minimal Changes:** Perform surgical updates. Avoid unrelated refactoring or "cleanup" unless explicitly requested.

## Style Preferences
- **Python:** Follow PEP 8. Use `ruff` for linting/formatting if available.
- **Web/TS:** Use modern ESM. Prefer Vanilla CSS for styling unless otherwise specified.
- **Commit Messages:** Clear, concise, and focused on "why" rather than "what".

## gstack
Use /browse from gstack for all web browsing.
Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /retro, /investigate, /document-release, /codex, /cso, /autoplan, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade.