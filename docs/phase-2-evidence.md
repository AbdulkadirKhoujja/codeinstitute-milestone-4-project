# Phase 2 verification record

Only commands actually executed are recorded here. No application tests existed at the baseline.

## Runtime recovery — 17 October 2026

- Baseline `821e2b0` on `main`, clean; fetched origin and confirmed 0 commits ahead/behind.
- uv 0.12.17's self-update route is unavailable for the bundled installation.
- The SHA-256-verified python.org installer exited 5 inside the sandbox in the preceding task.
- Downloaded the official `python` 3.13.16 NuGet package. Registration and catalog metadata identify the Python Software Foundation and CPython repository. The package's SHA-512 matched the catalog before extraction:
  `TGEhuRTpWtRifDR4r/GEhmg/cGMqtwB4kOCkt1QhXnCmdDE3Dict3iLJI1xrsNSRbXGyCwLEhe6qa5Rd2s376w==`.
- Runtime extracted outside Git at `%LOCALAPPDATA%\SkillSeat\runtimes\python-3.13.16\package\tools\python.exe`.
- `uv venv --python <that absolute executable> .venv`: exit 0.
- `uv pip install --python .venv/Scripts/python.exe -r requirements.txt`: exit 0.
- Interpreter assertions: Python 3.13.16, Django 5.2.18, executable inside this repository's `.venv`: exit 0.
- `uv pip check --python .venv/Scripts/python.exe`: exit 0, four compatible packages.
- `.venv` is ignored by `.gitignore:157`; `git ls-files .venv` is empty.
- Sandbox denied runtime-directory and uv cache writes. Approved command execution was used; no security settings, PATH entries, or existing Python installations were changed.
- Git push dry run succeeded. `gh auth status` reported an invalid token; CI access still needs verification.
- `scripts/Install-Python.ps1` independently reran metadata/hash/version verification successfully (exit 0).

## Environment validation TDD

- Red: `.venv/Scripts/python.exe -m unittest tests.test_environment -v`, exit 1: `ModuleNotFoundError: No module named 'config'`. Tests were committed before implementation.
- Green: same command, exit 0, 12 tests passed after implementing strict environment parsing.
- Contracts cover production defaults, explicit development mode, missing/weak keys, invalid debug values, production debug rejection, host validation, and avoiding secrets in configuration representations.
