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

## Django wiring TDD

- Red: `DJANGO_SETTINGS_MODULE=config.settings python -m django test tests.test_foundation -v 2`, exit 1: settings module did not exist.
- Django's `startproject config` rejected the existing config package. Generated the standard scaffold under a temporary name inside ignored `.venv/scaffold`, then copied manage.py/ASGI/WSGI with the final package name. The generated secret/settings stayed ignored; the tracked settings use validated environment input.
- Green: `python manage.py test -v 2`, 21 tests passed. `python manage.py check`, exit 0, no issues.
- Tests verify public routing/template, 404s, host rejection, app registration, SQLite connectivity and migrations, settings, ASGI, and WSGI.

## Authentication TDD

- Red: `python manage.py test tests.test_accounts -v 1`, exit 1, 12 tests: 1 failure (`auth.User` instead of `accounts.User`) and 7 errors (accounts namespace absent). Four inherited Django contracts already passed.
- Implemented `accounts.User(AbstractUser)`, configured it before the first persistent migration, generated `accounts/0001_initial`, and added Django login/logout views plus an authenticated own-account page.
- Green: `python manage.py test -v 1`, exit 0, all 33 tests passed in 5.456 seconds.
- Real password hashing, inactive-user rejection, CSRF, POST-only logout/session termination, safe login redirects, anonymous access, and non-staff admin rejection are covered.
- No registration, owner role, workshop, booking, review, payment, or resource models exist yet.

## Security and migration verification

- Added nine verification tests against the existing security implementation, not a manufactured Red cycle. `python manage.py test tests.test_security -v 2`: exit 0, nine passed in 5.637 seconds. Subprocess tests load real production/development settings and reject invalid startup configuration; response tests check HTTPS redirection, HSTS, framing/content-type headers, and session policy.
- `python manage.py migrate --noinput`: exit 0; all 19 initial Django/accounts migrations applied to ignored local SQLite.
- `python manage.py makemigrations --check --dry-run`: exit 0, no changes detected.
- `python manage.py migrate --check`: exit 0. `showmigrations` lists every migration applied.
- With production mode, generated transient key, explicit example host, debug off: `python manage.py check --deploy --fail-level WARNING`: exit 0, no issues, none silenced.
- HTTPS, HSTS (one year, subdomains, preload directive), secure cookies, CSRF, and frame denial are configuration foundations. No TLS terminator, production database, domain, or deployment has been provisioned.

## Reproducible dependencies and code quality

- Generated universal hash locks with uv 0.12.17 for runtime and development requirements. Runtime pins remain Python 3.13.16 and Django 5.2.18; resolved transitive packages are asgiref 3.12.1, sqlparse 0.6.0, and Windows tzdata 2026.5.
- Read official PyPI metadata and selected Ruff 0.17.1 as the only additional development tool. Hash-verified installation from both lock files succeeded (exit 0).
- Initial Ruff checks found three import-order issues and ten files needing formatting. Applied the formatter/import fixes, then `ruff check .` and `ruff format --check .` passed. This is tooling verification/refactoring, not application TDD.
- Post-format full suite: 42 tests passed in 10.982 seconds, exit 0.
- Real development-server smoke check: the sandbox attempt timed out with no response/log; approved execution outside the sandbox passed (exit 0), HTTP 200 with the expected home page. The child server was terminated by the script.
- Independently created `.venv/repro-check` using the NuGet executable's standard `-m venv`, installed both hash locks with pip, and ran pip integrity/version assertions: exit 0, Python 3.13.16 and Django 5.2.18. This validates the alternative setup used by CI.

## Continuous integration

- Added a Windows GitHub Actions workflow reproducing official NuGet setup, hashes, exact versions, dependency checks, lint/format, system/tests/migrations, production security checks, real-server smoke, and clean-tree checks.
- Verified official GitHub release metadata for checkout v7.0.1 (`3d3c42e5aac5ba805825da76410c181273ba90b1`); pinned that commit with read-only permissions and checkout credentials disabled.
- GitHub execution remains pending until this workflow is pushed and its actual result inspected.
