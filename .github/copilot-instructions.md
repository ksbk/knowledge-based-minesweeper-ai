# Copilot instructions

- Keep changes narrowly scoped to the requested solver, API, UI, or documentation task.
- Start with named files and direct tests; avoid repository-wide exploration unless necessary.
- Use `uv` and the Makefile. Prefer targeted pytest/Ruff checks while iterating; run `make check` once at the end when appropriate.
- Preserve deterministic reasoning behavior and existing knowledge/inference semantics.
- Run examples or browser/UI flows only when the changed surface requires them.
- Do not rerun unchanged successful checks or reinstall dependencies unnecessarily.
- Do not use GitHub Actions as a debugging loop; validate locally and batch pushes.
- Reuse existing abstractions rather than adding parallel implementations.
- Avoid unrelated refactors or speculative features.
- Stop when the requested outcome and relevant checks pass.