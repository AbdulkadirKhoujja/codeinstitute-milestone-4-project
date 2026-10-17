# SkillSeat

SkillSeat is the working title for a Code Institute Milestone Project 4 full-stack Django application.

## Project overview

This repository contains the Django foundation for SkillSeat. Workshop discovery and booking remain planned Phase 3 functionality. This README distinguishes verified foundation behaviour from planned product features.

## Purpose and intended audience

SkillSeat is planned as a full-stack Django workshop and training discovery and booking platform. It is intended to help people discover relevant workshops, register and manage participation, and access resources associated with paid attendance.

The intended audiences are:

- public visitors discovering workshops;
- registered attendees booking workshops and managing their participation; and
- workshop owners and administrators managing listings and related workflows.

## Current development status

- Phase 1 is complete: repository security, product definition, and documentation foundations have been committed and verified. Phase 2 has begun with the Python and Django dependency baseline.
- Python 3.13.16 and Django 5.2.18 are installed and verified in the ignored project `.venv`. Phase 2 foundation work is underway; verification evidence is recorded in [the Phase 2 log](docs/phase-2-evidence.md).
- Django is initialised with `config`, `core`, and `accounts` packages, SQLite configuration, ASGI/WSGI entry points, and 42 passing foundation tests. A custom user, sign-in/sign-out, and an authenticated own-account page establish the authentication foundation.
- Workshop features, screenshots, and deployment remain unimplemented.
- The README will be updated alongside the application and verification evidence.

## Planned product scope

The following is the committed core scope. Every item is planned and requires implementation and verification before it can be described as complete:

- public workshop discovery and workshop detail pages;
- registration, login, logout, and account management;
- workshop listing management for authorised owners and administrators;
- booking, cancellation, and server-enforced capacity controls;
- attendee reviews;
- Stripe test-mode payments with a verified payment state; and
- access-controlled workshop resources for paid attendees.

No optional enhancements are committed at this stage. They will only be considered after the core scope, tests, accessibility evidence, and documentation are complete.

## User stories and acceptance criteria

These concise stories define the initial testable scope. They are planning requirements, not evidence of implemented functionality.

### Committed core stories

**P0 — Anonymous visitor discovers a workshop**

As a public visitor, I want to browse workshops and open their details so that I can decide whether a workshop is relevant to me.

Acceptance criteria:

- workshop discovery is available without authentication;
- a workshop detail view presents the information needed to evaluate it; and
- an unavailable or invalid workshop does not expose unrelated records or internal errors.

**P0 — Visitor creates and uses an attendee account**

As a visitor, I want to register, sign in, sign out, and manage my account so that my participation is associated with my own identity.

Acceptance criteria:

- registration validates required input and does not reveal sensitive account information;
- login and logout provide clear success or failure states; and
- account actions cannot be used to access another attendee's account.

**P0 — Attendee books within capacity**

As an authenticated attendee, I want to book an available workshop so that I can reserve a place.

Acceptance criteria:

- only authenticated attendees can create bookings;
- a booking cannot increase attendance beyond the workshop capacity;
- concurrent booking attempts must respect the final available seat without overselling, with automated concurrency verification required during implementation;
- repeated booking attempts do not create duplicate active bookings for the same attendee and workshop; and
- the attendee can see the resulting booking state.

**P0 — Attendee cancels their booking**

As an authenticated attendee, I want to cancel my own booking so that my place can become available to someone else.

Acceptance criteria:

- an attendee can cancel only their own eligible booking;
- cancellation releases the reserved capacity according to the implemented booking rules; and
- an attendee cannot cancel or alter another attendee's booking.

**P0 — Attendee pays with verified test-mode payment**

As an attendee, I want to pay through Stripe test mode so that a paid booking has a trustworthy payment state.

Acceptance criteria:

- payment uses Stripe test credentials and never exposes secret credentials in client-side code or Git history;
- a booking is not treated as paid solely because a client reports success;
- the server records payment as verified only after the agreed Stripe confirmation flow;
- failed, cancelled, or expired payment attempts cannot permanently consume workshop capacity;
- the booking hold, payment expiration, and capacity-release policy is explicitly documented and tested during implementation;
- payment confirmation is verified server-side; and
- repeated provider notifications are handled idempotently and cannot process the same payment twice.

**P1 — Paid attendee accesses workshop resources**

As an attendee with a verified paid booking, I want to access the resources for that workshop so that I can prepare for or continue my training.

Acceptance criteria:

- access is granted only for the relevant workshop and verified paid booking;
- anonymous users, unpaid attendees, and attendees without the relevant booking are denied; and
- owners and administrators can manage resource access without exposing unrelated private resources.

**P1 — Attendee submits a review**

As an eligible attendee, I want to submit a review for a workshop I attended so that I can record useful feedback.

Acceptance criteria:

- a confirmed booking alone does not establish review eligibility before the workshop has taken place;
- review eligibility follows a documented attendance or completion policy and is enforced and tested server-side;
- an eligible authenticated attendee can submit one review for that workshop;
- an attendee can manage only their own review for that workshop; and
- review content is validated and displayed according to the moderation and visibility rules defined during implementation.

**P0 — Workshop owner manages their listings**

As a workshop owner, I want to create and manage my own workshop listings so that the public information remains accurate.

Acceptance criteria:

- an authorised owner can create, edit, publish, unpublish, or otherwise manage only their own listings;
- submitted ownership is assigned or verified server-side; and
- one owner cannot read or modify another owner's protected management data.

**P1 — Owner or administrator manages related workflows**

As an authorised workshop owner or administrator, I want to manage capacity, bookings, and workshop resources within my authority so that the platform remains operational.

Acceptance criteria:

- owners are restricted to workshops they own;
- administrators can perform the explicitly defined administrative actions across the platform;
- capacity changes cannot create an invalid overbooked state; and
- every protected action enforces authorization on the server, not only in the interface.

**P0 — Platform protects role and data boundaries**

As a platform maintainer, I want permission checks and payment state checks to be enforced server-side so that private data and paid resources are not disclosed.

Acceptance criteria:

- anonymous users cannot access authenticated, owner, administrator, or paid-resource actions;
- attendees cannot perform owner or administrator actions;
- owners cannot cross their ownership boundary;
- object-level authorization is covered by tests; and
- invalid identifiers, forged form data, replayed requests, and altered client-side payment states fail safely.

## Development phases

Development will remain within four phases. Implementation will follow strict Red → Green → Refactor TDD, with many small, meaningful commits that keep code, tests, and documentation aligned.

### Phase 1: Repository Foundation

Objective: establish a safe, documented, reviewable project baseline.

Deliverables: repository protections, the product direction, prioritised user stories, four-phase plan, and the documentation roadmap.

Completion criteria: only safe project foundations are committed; no secrets or local artefacts are tracked; the README distinguishes planned scope from implemented evidence; and independent review can verify the baseline.

### Phase 2: Django Foundation

Objective: create the smallest working Django foundation needed for tested development.

Deliverables: project configuration, dependency definitions, environment configuration guidance, initial application structure, initial data model decisions, and the first Red → Green → Refactor test slices.

Completion criteria: the foundation runs locally, configuration is documented, initial security boundaries are tested, and no feature is described as complete without passing evidence.

### Phase 3: Core SkillSeat Features

Objective: implement the committed discovery, account, workshop management, booking, capacity, review, payment, and resource-access scope.

Deliverables: incremental models, views, templates, forms, permissions, payment integration, resources, tests, design evidence, and documentation updates.

Completion criteria: each committed user story has passing relevant tests, including permission, capacity, and payment-state cases; responsive and accessible behaviour has evidence; and documentation matches the implementation.

### Phase 4: Release and Evidence

Objective: prepare, verify, and honestly document a releasable application.

Deliverables: production configuration, deployment evidence, security review, Git-history secret scanning, browser and accessibility checks, final screenshots, known limitations, credits, and reflection.

Completion criteria: release checks are reproducible, deployment claims are supported by recorded evidence, unresolved limitations are explicit, and the final README makes no unsupported claims.

## Documentation roadmap

Documentation will evolve with the real implementation. Planned documentation includes:

- wireframes and design rationale, with planned-versus-final comparisons for major journeys;
- data model entities, relationships, constraints, migrations, and ownership rules;
- routes, permissions, protected resources, and user journeys;
- technology choices, dependency rationale, and version records;
- local setup, environment configuration, and safe test credentials guidance;
- unit, integration, permission, payment, and browser testing evidence;
- responsive design decisions and accessibility evidence across relevant views;
- deployment steps, production configuration, and verification results;
- security review, including Git-history secret scanning and authorization boundaries; and
- known limitations, credits, and an honest reflection on decisions, challenges, and learning.

## Design and wireframes

Design evidence will be prominent and traceable. For each major journey, the README will distinguish the original planning artefact, the implemented result, and the comparison between them. If a wireframe or final capture does not exist, that absence will be stated rather than reconstructed retrospectively. No wireframes or screenshots are available yet.

## Features

The foundation provides a public status page, Django sign-in, POST-only sign-out, an authenticated own-account page, and staff-restricted Django admin. No Phase 3 workshop or booking features are implemented. Registration and account management remain planned.

## Data model

`accounts.User` subclasses Django's `AbstractUser` without adding fields. Username-based authentication, password hashing, groups, permissions, staff status, and superuser status retain Django's behaviour. `AUTH_USER_MODEL` is set before the initial persistent database migration. This small extension point avoids the disruption of swapping user models later; it does not invent owner or attendee role fields prematurely. Future foreign keys must use `settings.AUTH_USER_MODEL`, and runtime code must use `get_user_model()`. `accounts/0001_initial.py` creates the user and permission/group relationships. Workshop and booking entities remain undecided and unimplemented.

## Application architecture

`config/` contains environment validation, settings, root URLs, ASGI, and WSGI. `core/` owns the public foundation page; `accounts/` owns the custom user, admin registration, and minimal authentication routes. Shared templates live in `templates/`, and foundation tests in `tests/`. SQLite is appropriate for the local foundation; production database and concurrent booking decisions remain later work. There are no services, payment integrations, or additional business apps yet.

## Routes

| Route | Name | Access |
| --- | --- | --- |
| `/` | `core:home` | Public foundation page |
| `/accounts/login/` | `accounts:login` | Public sign-in, CSRF-protected POST |
| `/accounts/logout/` | `accounts:logout` | POST with CSRF token |
| `/accounts/` | `accounts:profile` | Authenticated user's own identity |
| `/admin/` | `admin:index` | Active staff users with Django permissions |

## Technology stack

The dependency foundation uses Python 3.13.16 and Django 5.2.18 LTS. The Python runtime is recorded in `.python-version` and the Django runtime dependency is pinned in `requirements.txt`. Django's built-in test runner runs the foundation tests; Ruff 0.17.1 provides linting and formatting. Hash locks freeze runtime and development packages. Stripe, PostgreSQL drivers, frontend packages, and hosting dependencies will be added only when required by later implementation work.

## Local setup

### Windows runtime and virtual environment

Use Python **3.13.16** and Django **5.2.18**. The verified Windows x64 fallback is the official [Python NuGet distribution](https://docs.python.org/3.13/using/windows.html#the-nuget-org-packages). It extracts into a dedicated per-user directory without an installer, administrator privileges, PATH changes, or changes to existing Python installations.

From PowerShell in this repository, with uv installed:

```powershell
.\scripts\Install-Python.ps1
$python = Join-Path $env:LOCALAPPDATA 'SkillSeat\runtimes\python-3.13.16\package\tools\python.exe'
uv venv --python $python .venv
uv pip install --python .venv/Scripts/python.exe --require-hashes -r requirements.lock -r requirements-dev.lock
.venv/Scripts/python.exe -c "import sys, django; print(sys.version); print(sys.executable); print(django.get_version())"
uv pip check --python .venv/Scripts/python.exe
```

The script validates package identity and SHA-512 against official NuGet catalog metadata before extracting or executing it. Keep the extracted runtime: the virtual environment depends on it. NuGet runtimes are replaced with a newly verified version rather than updated in place. Do not use the embeddable distribution for this setup.

The standard-library alternative has also been verified in a separate clean environment: replace the uv environment/install commands with `& $python -m venv .venv`, then `.venv/Scripts/python.exe -m pip install --require-hashes -r requirements.lock -r requirements-dev.lock` and `.venv/Scripts/python.exe -m pip check`. Choose one setup route for a new environment; do not recreate a working environment unnecessarily. Activation is optional because every command names its interpreter explicitly.

Configuration validation is implemented in `config/environment.py`. Production is the default; development must be selected explicitly. A strong `DJANGO_SECRET_KEY` is required in both modes. Production rejects debug mode and requires explicit allowed hosts. Missing, placeholder, or invalid values fail before the application starts. `.env.example` documents placeholders; it is not automatically loaded.

Configure the current PowerShell session, then run checks or the local server:

```powershell
$env:DJANGO_ENV = 'development'
$env:DJANGO_SECRET_KEY = .venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py test -v 2
.venv/Scripts/python.exe manage.py runserver 127.0.0.1:8000
```

The generated development key is ephemeral; use a stable private key in your local environment when preserving sessions. The database is local SQLite at ignored `db.sqlite3`. The custom user model is already configured; initialise the database with `.venv/Scripts/python.exe manage.py migrate`. Create a local administrator only when needed using `manage.py createsuperuser`; no credentials are shipped. Database migration checks are recorded in the evidence log when executed.

uv 0.12.17 predates this Python build and cannot download it from its bundled list. Passing the exact NuGet executable avoids that limitation. The full installer previously exited with access denied inside the restricted sandbox. If a managed environment denies network, cache, external-directory, or loopback-server access, use its approved permission mechanism; do not disable security controls. In a normal user PowerShell session, this route needs no Windows installer.

### Environment variables

| Variable | Development | Production |
| --- | --- | --- |
| `DJANGO_ENV` | Set explicitly to `development` | Defaults to `production` |
| `DJANGO_SECRET_KEY` | Required, generated private value | Required, stable private value |
| `DJANGO_DEBUG` | Defaults to `true`; accepts `true`, `false`, `1`, `0` | Defaults to `false`; enabling it is rejected |
| `DJANGO_ALLOWED_HOSTS` | Defaults to `localhost,127.0.0.1,[::1]` | Required comma-separated explicit hostnames |

Keys must contain at least 50 characters and five distinct characters; known placeholder prefixes are rejected. Generate a random key rather than merely satisfying those checks. Host values must not contain a URL scheme, port, wildcard, or empty entry. Unknown environment names fail instead of silently choosing a mode. No database URL, proxy trust, payment credentials, email service, or production service configuration is implemented in Phase 2.

`requirements.txt` remains the approved Django pin. `requirements.lock` additionally freezes its transitive dependencies with hashes and a Windows marker for `tzdata`. `requirements-dev.txt`/`.lock` add only Ruff 0.17.1 for linting and formatting. Install from the lock files for reproducibility. When deliberately updating dependencies, regenerate with `uv pip compile requirements.txt --universal --generate-hashes --output-file requirements.lock` and the equivalent command for `requirements-dev.txt`; review and test the resulting diff. Do not change the approved runtime pins incidentally.

## Testing

The built-in Django runner currently passes **42 tests**: 12 environment contracts, nine Django wiring/database checks, 12 authentication/model boundaries, and nine startup/security checks. Real Red/Green runs and the subsequent formatting refactor are recorded in [the evidence log](docs/phase-2-evidence.md). Tests use an isolated in-memory database and real password hashing. Production startup is also exercised in fresh subprocesses.

With development environment variables set as above:

```powershell
.venv/Scripts/ruff.exe check .
.venv/Scripts/ruff.exe format --check .
uv pip check --python .venv/Scripts/python.exe
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py test -v 2
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
.venv/Scripts/python.exe manage.py migrate --noinput
.venv/Scripts/python.exe manage.py migrate --check
.venv/Scripts/python.exe scripts/smoke_server.py
git diff --check
```

The smoke script starts the real development server on a temporary loopback port, verifies HTTP 200 and the SkillSeat page, then stops its child process. This passed with approved execution outside the restricted sandbox after the sandbox attempt timed out. The local database has all 19 initial migrations applied; fresh test databases also apply them successfully. No migration drift is detected.

Check production configuration in a separate shell (the example host is check-only, not a deployed site):

```powershell
$env:DJANGO_ENV = 'production'
$env:DJANGO_DEBUG = 'false'
$env:DJANGO_ALLOWED_HOSTS = 'skillseat.example.com'
$env:DJANGO_SECRET_KEY = .venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
.venv/Scripts/python.exe manage.py check --deploy --fail-level WARNING
```

This deployment check passes without silencing checks. It does not verify a real TLS endpoint, proxy, production database, or hosting platform. Browser, accessibility, payment, capacity, and workshop permissions require later implementation and verification.

### Continuous integration

`.github/workflows/foundation.yml` runs on pushes and pull requests to `main`, and supports manual runs. A Windows runner verifies the official NuGet runtime, creates a fresh environment, installs hash-locked dependencies, asserts exact versions and interpreter location, checks dependency integrity, runs lint/format/system/tests/migrations/production checks, and smoke-tests the server. The checkout action is pinned to an immutable official release commit, permissions are read-only, and no repository secret is required. A random check-only key is generated per run. Actual GitHub execution results will be linked in the evidence log once verified.

## Deployment

SkillSeat has not been deployed. Deployment targets, production configuration, release steps, and verification evidence will be documented after they are decided and tested.

## Security

Secrets, credentials, local databases, environment files, uploads, and generated deployment artefacts must not enter Git history. `.gitignore` protects local artefacts. Production defaults enforce HTTPS redirects, secure session/CSRF cookies, HTTP-only sessions, SameSite Lax, frame denial, content-type protection, and one-year HSTS with subdomains and the preload directive. Do not use production mode on a plain-HTTP development server. Before deployment, confirm that the real domain and every subdomain support HTTPS; the directive does not itself submit a domain to a preload list. Forwarded proxy headers are deliberately not trusted until a specific deployment is configured.

Missing/weak secrets, production debug mode, malformed booleans, and missing/invalid hosts prevent startup. Django's standard password validators and model permissions are retained. Anonymous account requests redirect to login; ordinary users cannot enter admin. Sign-in and POST-only sign-out enforce CSRF. Production `check --deploy --fail-level WARNING` currently passes without silencing checks. Production infrastructure and later object-level permissions still require their own tests and release review.

## Accessibility

Accessibility requirements, responsive implementation decisions, and manual or automated evidence will be recorded here. No accessibility verification has been completed yet.

## Limitations

The Django foundation is implemented and tested; workshop features are not. SQLite validation does not demonstrate production concurrency safety. Login has Django's standard authentication behaviour but no rate-limiting infrastructure yet. Production database, HTTPS termination, trusted proxy configuration, domain-specific policy, email delivery, registration, owner permissions, and all booking/payment/resource rules remain later work. No deployment, wireframes, screenshots, browser-based usability review, or accessibility audit is claimed. The Windows x64 setup is verified; other operating systems are not yet verified.

## Credits

SkillSeat is a Code Institute Milestone Project 4 repository. Foundation references: [Python's official Windows/NuGet guidance](https://docs.python.org/3.13/using/windows.html#the-nuget-org-packages), [Django's early custom-user guidance](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project), [Django's deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/), [Ruff](https://docs.astral.sh/ruff/), and [GitHub's checkout action](https://github.com/actions/checkout). Project/ASGI/WSGI boilerplate and the initial user migration were generated by Django 5.2.18 and adapted to this configuration.

## Reflection

Phase 2 showed why runtime availability must be proved separately from dependency compatibility: the approved versions were compatible, but the bundled uv download list and sandboxed installer prevented installation. Verifying the official NuGet package against its catalog hash provided an isolated runtime without replacing existing installations. Authentication was decided before persistent migrations, and test-first environment/routing/authentication increments preserved evidence of actual failures and fixes. Production checks are useful configuration evidence, but they do not substitute for deployment validation.
