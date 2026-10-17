# SkillSeat

SkillSeat is the working title for a Code Institute Milestone Project 4 full-stack Django application.

## Project overview

SkillSeat is a Django workshop discovery and booking application. Phase 3 implements the committed core features, with real database, permission, concurrency and browser evidence. Genuine Stripe sandbox transaction verification remains an external dependency; Phase 3 is not yet declared fully complete.

## Purpose and intended audience

SkillSeat helps people discover practical workshops, manage their participation, and access private learning resources after verified paid booking.

The intended audiences are:

- public visitors discovering workshops;
- registered attendees booking workshops and managing their participation; and
- workshop owners and administrators managing listings and related workflows.

## Current development status

- Phases 1 and 2 are verified. Phase 3 core implementation is present; final external payment verification remains outstanding. Phase 4 has not begun.
- Python 3.13.16 and Django 5.2.18 are installed and verified in the ignored project `.venv`. Runtime recovery, test-first increments, migration checks, CI, and limitations are recorded in [the Phase 2 log](docs/phase-2-evidence.md).
- The established custom user and production security defaults are preserved. `workshops` adds discovery, controlled ownership, atomic bookings, test-only Checkout, private resources and attendance-gated reviews.
- The unchanged baseline passed 42 tests before development. The expanded suite and separate file-backed SQLite races are recorded in [Phase 3 evidence](docs/phase-3-evidence.md). The obsolete foundation home-page planning assertion now checks the working discovery link; no foundation test case was deleted.
- Planning wireframes and real browser captures are separate in [design evidence](docs/design/phase-3-verification.md). No production deployment has occurred.

## Planned product scope

The following committed core scope now has implementation and automated evidence. A genuine external Stripe transaction is still required before the payment story and Phase 3 can be called fully verified:

- public workshop discovery and workshop detail pages;
- registration, login, logout, and account management;
- workshop listing management for authorised owners and administrators;
- booking, cancellation, and server-enforced capacity controls;
- attendee reviews;
- Stripe test-mode payments with a verified payment state; and
- access-controlled workshop resources for paid attendees.

No optional enhancements are committed at this stage. They will only be considered after the core scope, tests, accessibility evidence, and documentation are complete.

## User stories and acceptance criteria

These stories define the agreed acceptance requirements. The [acceptance evidence map](docs/phase-3-architecture.md#acceptance-evidence-map) connects each story to implementation and real tests, and identifies the external payment gap.

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

Status: verified with 42 passing tests, applied initial migrations, no migration drift, production configuration checks, a real-server smoke check, and a successful Windows CI run. The development history retains separate failing-test and passing-implementation commits; see [the ordered evidence record](docs/phase-2-evidence.md#commit-evidence).

### Phase 3: Core SkillSeat Features

Objective: implement the committed discovery, account, workshop management, booking, capacity, review, payment, and resource-access scope.

Deliverables: incremental models, views, templates, forms, permissions, payment integration, resources, tests, design evidence, and documentation updates.

Completion criteria: each committed user story has passing relevant tests, including permission, capacity, and payment-state cases; responsive and accessible behaviour has evidence; and documentation matches the implementation.

Status: core implementation and automated/browser verification are documented in [Phase 3 evidence](docs/phase-3-evidence.md). Completion is withheld pending genuine Stripe sandbox verification. Phase 4 remains release/deployment work and has not started.

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

The [original planning wireframes](docs/design/phase-3-wireframes.md) were committed before business interface implementation. [Final design verification](docs/design/phase-3-verification.md) links real screenshots, browser journeys, viewport measurements, accessibility observations and planned-versus-implemented differences. These are separate artefacts; generated visual mockups are not used as evidence of working screens.

## Features

- Public upcoming published-workshop cards and details with host, UTC schedule, location, price and current seats. Past details remain available for reviews, with booking closed.
- Registration, sign-in/out, own-profile editing and password changes using Django authentication and validation.
- Permission-provisioned owner studio: create/edit/publish/unpublish, safe capacity changes, booking roster, attendance and private resource upload/removal. Superusers can work across owners.
- Own booking history, free confirmation, paid pending holds, cancellation and executable expiry cleanup, with database-backed capacity and duplicate protections.
- Stripe test-only hosted Checkout, server price snapshots, signed event verification, durable replay protection and explicit late-payment refund review. Offline tests pass; a real provider transaction remains unverified.
- Authorised private downloads for relevant verified-paid confirmed attendees; files have no public media URL.
- Reviews only after workshop completion and owner-recorded attendance, own editing/deletion and superuser visibility moderation.
- Shared responsive styling, accessible labels/help/errors, skip navigation, keyboard focus and clear server-state feedback.

## Data model

`accounts.User` retains the Phase 2 AbstractUser model and Django's password/group/permission behaviour. All user references use AUTH_USER_MODEL. Workshop, Booking, PaymentAttempt, PaymentEvent, Resource and Review form the core domain. Prices use integer GBP pence; dates are aware UTC. Database constraints enforce capacity, date ordering, active-booking uniqueness, valid states and ratings. See the [relationship diagram, constraints and state machines](docs/phase-3-architecture.md).

## Application architecture

`config/` owns validated settings and entry points; `core/` owns the public landing page, shared CSS and response headers; `accounts/` owns the custom user and account workflows. `workshops/` owns models, forms, scoped views, private storage, transactional booking services, Stripe integration and management commands. Templates remain conventional Django HTML with CSS, with no frontend framework or external font dependency. Tests live in `tests/`. SQLite shared-memory and file-backed independent-connection races are verified; production PostgreSQL is not tested. [Operating policies](docs/phase-3-architecture.md) explain the guarantees and limits.

## Routes

| Route | Name | Access |
| --- | --- | --- |
| `/` | `core:home` | Public discovery landing page |
| `/accounts/login/` | `accounts:login` | Public sign-in, CSRF-protected POST |
| `/accounts/logout/` | `accounts:logout` | POST with CSRF token |
| `/accounts/` | `accounts:profile` | Authenticated user's own identity |
| `/admin/` | `admin:index` | Active staff users with Django permissions |

The [complete Phase 3 route/permission table](docs/phase-3-architecture.md#roles-routes-and-boundaries) covers registration, account editing, studio, bookings, checkout, signed webhooks, resources and reviews.

## Technology stack

Python 3.13.16 and Django 5.2.18 LTS are unchanged. Django's test runner and Ruff 0.17.1 remain the tools. Stripe SDK 16.0.0 is deliberately added, with its HTTP/typing dependencies hash-locked in requirements.lock. Its API version is explicitly pinned to `2026-09-30.endive`. No PostgreSQL driver, frontend framework or hosting dependency is introduced. The optional Stripe CLI 1.54.0 was used locally to inspect sandbox provisioning; ignored local tooling is not needed by CI.

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
.venv/Scripts/python.exe manage.py migrate --noinput
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
| `STRIPE_TEST_KEY` | Private test restricted key; blank disables Checkout | Test mode only; live key prefixes refused |
| `STRIPE_WEBHOOK_SECRET` | Private listener signing secret | Private endpoint signing secret; no live events accepted |
| `PAYMENT_ORIGIN` | Defaults to `http://localhost:8000` | Explicit HTTPS origin for test return URLs |
| `SKILLSEAT_FILE_TEST_DB` | `1` selects ignored file-backed test DB for race verification | Test-only; leave unset for normal operation |

Keys must contain at least 50 characters and five distinct characters; known placeholder prefixes are rejected. Generate a random key rather than merely satisfying those checks. Host values must not contain a URL scheme, port, wildcard, or empty entry. Unknown environment names fail instead of silently choosing a mode. There is no email delivery/verification service, database URL loader or proxy trust. Stripe settings are environment-managed and never printed by application pages.

### Phase 3 local operation

After migrations, `manage.py seed_demo` creates three explicitly fictional workshops with a passwordless demo host (development only, idempotent). It does not create customers, payments or an administrator. Register your own attendee normally. A trusted administrator grants `workshops.add_workshop` through Django admin to provision an approved owner; registration never assigns it. Superusers manage all workshops through the studio and moderate reviews in admin.

Run `manage.py expire_bookings` to release unpaid 35-minute holds. Discovery/reservation/dashboard requests also perform cleanup. No background scheduler is assumed. Private uploads are stored under ignored `private-resources/`, with a 5 MB form limit and authorised attachment responses. Do not expose this folder through a web server. [Stripe setup and policies](docs/phase-3-architecture.md#stripe-test-mode-setup) explain hosted Checkout, signed local forwarding, pending/late events and manual test-refund review.

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

The smoke script starts the real development server on a temporary loopback port, verifies HTTP 200 and the SkillSeat page, then stops its child process. The full test suite includes the original foundation cases plus accounts, discovery, owners, bookings, payment signatures/states, resources, reviews, interface and real connection races. [Phase 3 evidence](docs/phase-3-evidence.md) records actual counts, migration results and command output summaries. For a separate file-backed race run, set `SKILLSEAT_FILE_TEST_DB=1`, run `manage.py test tests.test_concurrency -v 2 --noinput`, then remove that environment variable. Tests recreate only the ignored test database, not db.sqlite3.

Check production configuration in a separate shell (the example host is check-only, not a deployed site):

```powershell
$env:DJANGO_ENV = 'production'
$env:DJANGO_DEBUG = 'false'
$env:DJANGO_ALLOWED_HOSTS = 'skillseat.example.com'
$env:DJANGO_SECRET_KEY = .venv/Scripts/python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
.venv/Scripts/python.exe manage.py check --deploy --fail-level WARNING
```

This configuration check does not verify a real TLS endpoint, proxy, production database or hosting platform. Browser, accessibility, capacity, ownership and simulated payment evidence are recorded separately; genuine Stripe sandbox verification remains outstanding.

### Continuous integration

`.github/workflows/foundation.yml` runs on pushes and pull requests to `main`, and supports manual runs. A Windows runner verifies the official NuGet runtime, creates a fresh environment, installs hash-locked dependencies, asserts exact versions and interpreter location, checks dependency integrity, runs lint/format/system/tests/migrations/production checks, and smoke-tests the server. The checkout action is pinned to an immutable official release commit, permissions are read-only, and no repository secret is required. A random check-only key is generated per run.

[Phase 3 Windows CI run 39057049274](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39057049274) completed successfully on `c71bc8dcd10e296807f72248c0d5a706f4e76b57`, including all 109 tests at that checkpoint and the separate file-backed concurrency run. The final discovery edge-case correction increases the local suite to **110 passing tests**; the [consolidated report](docs/phase-3-report.md) and final delivery message identify final verification. The earlier Phase 3 lint failure is retained in the evidence; it was fixed without weakening checks. CI uses simulated Stripe fixtures and requires no payment secrets. This is verification, not deployment.

## Deployment

SkillSeat has not been deployed. Deployment targets, production configuration, release steps, and verification evidence will be documented after they are decided and tested.

## Security

Secrets, credentials, local databases, environment files, uploads, and generated deployment artefacts must not enter Git history. `.gitignore` protects local artefacts. Production defaults enforce HTTPS redirects, secure session/CSRF cookies, HTTP-only sessions, SameSite Lax, frame denial, content-type protection, and one-year HSTS with subdomains and the preload directive. Do not use production mode on a plain-HTTP development server. Before deployment, confirm that the real domain and every subdomain support HTTPS; the directive does not itself submit a domain to a preload list. Forwarded proxy headers are deliberately not trusted until a specific deployment is configured.

Missing/weak secrets, production debug mode, malformed booleans and missing/invalid hosts prevent startup. Django's password validators, safe login redirects, session handling and CSRF remain. Object-level owner/account/resource/review checks are enforced server-side and tested with forged identifiers and ownership fields. Capacity/financial audit admin is read-only; superusers moderate visibility. Signed webhooks are the only CSRF exemption. Test-mode event flags, exact server amounts and durable event receipts protect fulfillment. Private pages use no-store; application pages use a restrictive CSP. Production infrastructure still requires release review.

## Accessibility

WCAG 2.2 AA is the design target. Semantic landmarks/headings, a skip link, visible keyboard focus, explicit labels, associated help/errors, native controls, live status feedback and responsive wrapping are implemented. Actual browser measurements, keyboard observations, contrast calculations, captures and limitations are in [design verification](docs/design/phase-3-verification.md). Browser review found and fixed duplicate form IDs. These scoped checks do not establish full WCAG compliance or a screen-reader audit.

## Limitations

Genuine Stripe sandbox Checkout/payment/webhook forwarding remains unverified because no test credentials or signing secret are present. Official CLI provisioning requires an email/authenticated account; no user identity was transmitted automatically. The SDK initiation is mocked in tests and signature validation uses synthetic signed payloads. This gap prevents a full Phase 3 completion claim.

SQLite races are tested locally and in Windows CI, but PostgreSQL and production concurrency are not verified. Login has Django's normal behaviour without rate-limiting infrastructure. No email delivery, live payments, automatic refunds, background scheduler or production deployment is configured. Private local file delivery needs production storage/request-size/content controls before release. Accessibility evidence is scoped rather than a full compliance claim. Windows x64 is verified; other operating systems remain unverified. Phase 4 must handle production deployment, database/proxy/storage/scheduler configuration and comprehensive release evidence after the Phase 3 payment gap is resolved.

## Credits

SkillSeat is a Code Institute Milestone Project 4 repository. Foundation references: [Python's official Windows/NuGet guidance](https://docs.python.org/3.13/using/windows.html#the-nuget-org-packages), [Django's early custom-user guidance](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project), [Django's deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/), [Ruff](https://docs.astral.sh/ruff/), and [GitHub's checkout action](https://github.com/actions/checkout). Project/ASGI/WSGI boilerplate and the initial user migration were generated by Django 5.2.18 and adapted to this configuration.

Phase 3 used [Stripe Checkout creation](https://docs.stripe.com/api/checkout/sessions/create), [Checkout fulfillment](https://docs.stripe.com/checkout/fulfillment), [webhook signature validation](https://docs.stripe.com/webhooks), and the official [stripe-python SDK](https://github.com/stripe/stripe-python). The Stripe best-practices/documentation plugin skills informed the integration; public official documentation was used when the connected documentation tool repeatedly requested authentication. CSS artwork and fictional workshop descriptions are project-created. Real screenshots are from the local running application.

## Reflection

Phase 2 showed why runtime availability must be proved separately from dependency compatibility: the approved versions were compatible, but the bundled uv download list and sandboxed installer prevented installation. Verifying the official NuGet package against its catalog hash provided an isolated runtime without replacing existing installations. Authentication was decided before persistent migrations, and test-first environment/routing/authentication increments preserved evidence of actual failures and fixes. Production checks are useful configuration evidence, but they do not substitute for deployment validation.

Phase 3 made transaction boundaries concrete: independent SQLite connections exposed lock errors that sequential tests could not reveal. Atomic conditional counter updates, rollback and bounded lock retries preserve capacity without claiming SQLite row locking. Signed provider events, rather than redirects, determine payment access; late success deliberately becomes refund review. Browser inspection caught duplicate form IDs that ordinary view tests missed, leading to specific regression tests and semantic shared form rendering. A real CI failure also exposed an unstaged lint fix, reinforcing the need to verify staged content. The separate Red/Green commits and [chronological history](docs/phase-3-commits.md) preserve these actual development steps.
