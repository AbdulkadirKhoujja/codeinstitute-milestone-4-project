# SkillSeat

SkillSeat is a Code Institute Milestone Project 4 full-stack Django workshop discovery and booking application.

**[Visit the live SkillSeat application](https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/)**

Production: Heroku · PostgreSQL 18.4 · HTTPS · Stripe integration supports test mode only.

## Project overview

SkillSeat connects curious learners with small practical workshops. Visitors discover workshops; registered attendees reserve places and manage bookings; approved hosts publish workshops, record attendance and share protected resources. The application is deployed and its core hosted journeys are verified. Phase 3 retains a genuine Stripe sandbox payment and signed webhook record. The current Heroku deployment has no Stripe credentials configured, so hosted payment completion and paid-attendee resource access remain unverified. Phase 4 remains open until the outstanding release requirements are satisfied.

## Purpose and intended audience

SkillSeat helps people discover practical workshops, manage their participation, and access private learning resources after verified paid booking.

The intended audiences are:

- public visitors discovering workshops;
- registered attendees booking workshops and managing their participation; and
- workshop owners and administrators managing listings and related workflows.

## Current development status

- **Live:** [https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/](https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/). Existing Heroku app `skillseat-akkhoujja`, Europe, heroku-24, one Basic web dyno and its own Essential-0 PostgreSQL attachment. No additional resources were provisioned during this continuation; ByteBoard was not modified.
- Runtime verification snapshot: **release v19**, commit `e06fce0a855a650afd75469ffcd089a1469813b2`. Documentation publication uses the same runtime source; its exact final deployment SHA/release and final CI run are identified in the delivery record, avoiding a self-referential Git hash inside its own commit.
- **132 Django tests pass** locally and separately in Windows, PostgreSQL 17 and PostgreSQL 18 CI. Each full suite includes seven independent-connection races; Windows also runs seven file-backed SQLite races. Three custom JavaScript behavior tests pass.
- Hosted account, owner CRUD, discovery filters, final-seat concurrency, cancellation, request-triggered expiry, attendance/review CRUD, private owner downloads and denials, HTTPS/CSRF/throttling, static delivery and genuine restart persistence are verified with fictional fixtures. Temporary application records and authenticated fixture sessions were cleaned up afterwards.
- Hosted W3C HTML: four public pages, no messages. CSS: valid, zero errors, one system-font vendor warning. Hosted mobile Lighthouse: **100 performance / 100 accessibility / 100 best practices / 100 SEO**. These checks do not establish full WCAG compliance.
- The supplied **Unit 4 specification (F/650/3528, printed pp. 55–65)** and **13 mandatory requirements** now drive the [assessment matrix](docs/assessment-audit.md). Criterion 3.2 and mandatory requirement 8 exposed real gaps, corrected through Red/Green commits.
- **Remaining:** privately configure existing Stripe test credentials and the hosted webhook endpoint, then verify real payment/replay/late-event journeys and paid-attendee downloads. No scheduler is attached; no-traffic hosted expiration remains unverified. No submission-ready or grade claim is made.

## Implemented product scope

The following committed core scope now has implementation and automated evidence. The payment story also has genuine hosted sandbox payment, signed webhook, protected download and replay evidence:

- public workshop discovery and workshop detail pages;
- registration, login, logout, and account management;
- workshop listing management for authorised owners and administrators;
- booking, cancellation, and server-enforced capacity controls;
- attendee reviews;
- Stripe test-mode payments with a verified payment state; and
- access-controlled workshop resources for paid attendees.

Text/location search and free/paid discovery filters support workshop selection. Custom JavaScript asks before cancelling a booking; the server remains responsible for CSRF, ownership and eligibility, and the ordinary form also works without JavaScript.

## User stories and acceptance criteria

These stories define the agreed acceptance requirements. The [acceptance evidence map](docs/phase-3-architecture.md#acceptance-evidence-map) connects each story to implementation and real tests, and records the completed genuine sandbox exercise.

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

Status: core implementation and automated/browser verification are documented in [Phase 3 evidence](docs/phase-3-evidence.md). Genuine hosted sandbox payment, signed delivery, paid resource access and replay verification now pass. Phase 4 release/deployment work is now in progress; its independent checks and external blockers are recorded below.

### Phase 4: Release and Evidence

Objective: prepare, verify, and honestly document a releasable application.

Deliverables: production configuration, deployment evidence, security review, Git-history secret scanning, browser and accessibility checks, final screenshots, known limitations, credits, and reflection.

Completion criteria: release checks are reproducible, deployment claims are supported by recorded evidence, unresolved limitations are explicit, and the final README makes no unsupported claims.

## Documentation roadmap

The documentation below contains the implemented design, data model, operating rules and actual evidence:

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

## Actual production screenshots

These are real captures of the publicly hosted Heroku application on 19 October 2026. They are separate from the historical local captures below. Screens containing accounts/workshops use explicitly fictional temporary fixtures; `example.invalid` is not a real contact address. Fixtures were cleaned up after the checks, and the empty-state capture records the resulting production state. No credentials, payment secrets or private handout contents appear in these images. Screenshots represent verification releases v17/v19; the later authentication guard and cancellation-script additions do not alter the other captured layouts.

| Journey | Desktop production | Mobile production |
| --- | --- | --- |
| Homepage and navigation | ![Hosted desktop homepage](docs/design/production/home-desktop.jpg) | ![Hosted mobile homepage and wrapping navigation](docs/design/production/home-mobile.jpg) |
| Discovery and filters | ![Hosted workshop discovery with fictional listings](docs/design/production/discovery-desktop.jpg) | ![Hosted mobile text and paid-price filter controls](docs/design/production/discovery-filter-mobile.jpg) |
| Workshop details | ![Hosted desktop workshop detail and booking interface](docs/design/production/detail-desktop.jpg) | ![Hosted mobile workshop detail](docs/design/production/detail-mobile.jpg) |
| Registration | ![Hosted labelled desktop registration form](docs/design/production/register-desktop.jpg) | ![Hosted mobile registration form](docs/design/production/register-mobile.jpg) |
| Login | ![Hosted desktop sign-in form with no credentials entered](docs/design/production/login-desktop.jpg) | ![Hosted mobile sign-in form](docs/design/production/login-mobile.jpg) |
| Account | ![Hosted fictional owner profile and studio entry](docs/design/production/profile-desktop.jpg) | ![Hosted fictional attendee profile](docs/design/production/profile-mobile.jpg) |
| Booking states | ![Hosted pending booking with test-mode checkout control](docs/design/production/booking-pending-desktop.jpg) | ![Hosted confirmed and expired booking states](docs/design/production/bookings-mobile.jpg) |

The original discovery/detail planning expected a route from workshop cards to availability and booking; production preserves that journey and adds accessible search/price controls. The original account planning separated personal bookings from host management; the two real account captures show those permission-dependent entries. Original text-to-SVG wireframes remain embedded below, with their original source and later rendering dates explicit.

### Tablet and owner workflows

![Hosted tablet discovery](docs/design/production/discovery-tablet.jpg)
![Hosted owner studio with only the fictional owner's workshop records](docs/design/production/studio-desktop.jpg)
![Hosted tablet workshop editor](docs/design/production/owner-edit-tablet.jpg)
![Hosted private-resource controls and visible keyboard focus; no file contents exposed](docs/design/production/resources-tablet.jpg)

### Honest feedback, error and empty states

![Actual hosted feedback that Stripe test payments are not configured](docs/design/production/checkout-unconfigured-mobile.jpg)
![Actual successful hosted booking cancellation](docs/design/production/cancellation-desktop.jpg)
![Actual safe hosted 404 page with recovery navigation](docs/design/production/safe-404-desktop.jpg)
![Actual production discovery after temporary fictional data was cleaned up](docs/design/production/empty-discovery-desktop.jpg)

The [capture manifest](docs/testing/phase4-production-screenshots.json) records file dimensions and SHA-256 hashes. These are screenshots, not reconstructed designs. The dated original wireframes and local implementation history follow.

## Design and wireframes

The original planning artefact was committed on **17 October 2026 before implementation**. It contains text wireframes, rather than image files. The SVGs below were rendered from that unchanged text during Phase 4 on **19 October** using `scripts/render_planning.py`; the rendering dates are printed on the images. They are not retroactively invented historical image wireframes. **No separate original mobile image wireframes existed.** Mobile intent was documented as wrapping navigation, stacked cards/detail columns, labelled forms and touch-friendly controls.

| Journey | Original planning | Authentic implemented evidence | Outcome |
| --- | --- | --- | --- |
| Home/discovery/detail | Original desktop text, rendered below | Desktop home, mobile discovery, tablet detail | Clear discovery entry, cards and a booking sidebar; stacks on narrow screens |
| Account/booking/payment | Original journey text, rendered below | Registration, confirmed booking, pending/payment feedback | One account dashboard and explicit server payment state |
| Owner management | Original studio text, rendered below | Owner editing/roster/resource screen | Separate owner boundary, mobile-friendly sequential sections |
| Mobile | Responsive intent in the original text; no standalone image wireframe | Actual mobile home, discovery and registration | Navigation wraps; forms and cards remain within the viewport |

### Home, discovery and workshop details

**Planning evidence → implementation → outcome**

![Phase 4 rendering of SkillSeat's original 17 October desktop discovery and detail text wireframe](docs/design/wireframes/discovery-original-text.svg)

The following are authentic **local Django application** screenshots captured during Phase 3 verification, not Heroku screenshots. Hosted replacements cannot be claimed before deployment.

![Actual SkillSeat desktop homepage with custom ticket illustration and discovery action](docs/design/final/home-desktop.jpg)

![Actual SkillSeat mobile homepage with wrapped navigation and stacked layout](docs/design/final/home-mobile.jpg)

![Actual mobile workshop discovery with clearly fictional listings and prices](docs/design/final/discovery-mobile.jpg)

![Actual tablet workshop detail with schedule, host and booking context](docs/design/final/detail-tablet.jpg)

The final page retains the planned hierarchy but adds an original CSS ticket illustration and a three-step introduction. Workshop cards show fictional host, UTC schedule, GBP price and seats. Discovery now excludes started workshops; their published detail pages retain reviews without advertising bookable seats. Existing attendees are directed to their booking management rather than another reservation attempt.

### Accounts, bookings and payment states

![Phase 4 rendering of the original account booking and payment-state planning text](docs/design/wireframes/booking-original-text.svg)

![Actual mobile registration form with password guidance and labels](docs/design/final/register-mobile.jpg)

![Actual mobile free booking confirmation and cancellation control](docs/design/final/booking-confirmed-mobile.jpg)

![Actual pending paid booking with honest Stripe configuration feedback](docs/design/final/payment-unconfigured-tablet.jpg)

The final flow uses Django forms, own-account controls and clear state feedback. Browser review exposed duplicated labels and invalid help-text structure; unique resource IDs and block help with aria-describedby corrected them. The payment-error screenshot is a historical configuration-denial checkpoint, not a successful payment screenshot. Phase 3 subsequently completed the genuine hosted sandbox exercise. Checkout initiation guidance is now four minutes after reservation to retain Stripe's minimum session lifetime plus a safety margin.

### Owner studio and protected resources

![Phase 4 rendering of the original owner studio planning text](docs/design/wireframes/owner-original-text.svg)

![Actual owner workshop form with booking roster and private resource upload](docs/design/final/owner-edit-tablet.jpg)

The sequential edit → roster → resource layout replaces a dense table so controls remain usable on mobile. A trusted administrator grants the owner permission; form fields cannot assign ownership. Resource downloads always pass object-level checks. Private bytes now persist in the separately configured production database rather than an ephemeral dyno directory.

Release-specific local login, account dashboard, private-resource and review screenshots follow below. No original planning image or hosted result is invented to fill an evidence gap. Supplementary provenance and detailed observations remain in the design evidence, while these actual assets are embedded here for the assessor.

### Release journey evidence — local application, 19 October 2026

The following are authentic captures from the running local Django application. The owner, attendee, completed workshop and review are explicitly fictional verification fixtures; no attendance or payment by a real person is asserted. The host recorded attendance through the studio, the attendee then submitted an eligible review, and an unpaid direct-file request returned 404. An authorised host downloaded the exact fictional handout bytes through the browser. These are separate from the earlier genuine Stripe sandbox payment record.

![Local desktop sign-in form with explicit username and password labels](docs/design/release/login-desktop.jpg)
![Local owner account dashboard with own profile, bookings and studio entry](docs/design/release/account-owner-desktop.jpg)
![Local mobile private resource controls, authorisation notice and visible keyboard focus](docs/design/release/owner-private-resources-mobile.jpg)
![Local mobile eligible review with explicit simulated-event provenance and own edit/delete controls](docs/design/release/review-community-mobile.jpg)
![Actual branded missing-workshop page with debug disabled and safe navigation](docs/design/release/safe-404-desktop.jpg)

At 390px, owner and review pages had document width 375px and no horizontal overflow; keyboard focus is visible on the resource/review controls. The release journey also exposed a stale cancellation action on a completed workshop: the server already denied it, and a new Red/Green interface test now replaces that control with the cancellation deadline. On actual GitHub, all 11 original embedded images loaded at nonzero natural widths and all three Mermaid diagrams rendered; all 16 embedded images including the release captures were confirmed loaded in the actual GitHub render after pushing. No physical-device or screen-reader result is claimed.

## Features

- Public upcoming published-workshop cards and details with host, UTC schedule, location, price and current seats. Past details remain available for reviews, with booking closed.
- Registration, sign-in/out, own-profile editing and password changes using Django authentication and validation.
- Permission-provisioned owner studio: create/edit/publish/unpublish, safe capacity changes, booking roster, attendance and private resource upload/removal. Superusers can work across owners.
- Own booking history, free confirmation, paid pending holds, cancellation and executable expiry cleanup, with database-backed capacity and duplicate protections.
- Stripe test-only hosted Checkout, server price snapshots, signed event verification, durable replay protection and explicit late-payment refund review. Offline tests and a genuine £25 GBP hosted sandbox payment pass, including authenticated CLI forwarding, signed fulfillment, paid resource access and genuine-event replay protection. [Provider verification evidence](docs/phase-3-evidence.md#completed-manual-sandbox-payment--18-october-2026).
- Authorised private downloads for relevant verified-paid confirmed attendees; files have no public media URL.
- Reviews only after workshop completion and owner-recorded attendance, own editing/deletion and superuser visibility moderation.
- Shared responsive styling, accessible labels/help/errors, skip navigation, keyboard focus and clear server-state feedback.

## Data model

The established `accounts.User` remains a Django AbstractUser. All user relationships use AUTH_USER_MODEL. The diagram shows actual foreign-key relationships; PrivateResourceBlob and AuthThrottle are independent storage/operational tables.

```mermaid
erDiagram
    User ||--o{ Workshop : owns
    User ||--o{ Booking : reserves
    Workshop ||--o{ Booking : contains
    Booking ||--o| PaymentAttempt : tracks
    Workshop ||--o{ Resource : provides
    Workshop ||--o{ Review : receives
    User ||--o{ Review : writes
    Workshop {
        bigint id PK
        int capacity
        int reserved
        int price_pence
        datetime starts_at
        datetime ends_at
        boolean published
    }
    Booking {
        bigint id PK
        string status
        int amount_pence
        datetime expires_at
        boolean paid
        boolean attended
        boolean refund_required
    }
    PaymentEvent {
        string event_id UK
        string event_type
        datetime received_at
    }
    PrivateResourceBlob {
        string name PK
        binary content
        datetime created_at
    }
    AuthThrottle {
        string key PK
        int failures
        datetime expires_at
    }
```

| Constraint/decision | Application guarantee |
| --- | --- |
| Workshop capacity >=1 and reserved <= capacity | Counters cannot describe an oversold workshop |
| Ends after starts; aware UTC dates | Ordered schedules; every interface labels UTC |
| Integer GBP pence, 0 or 50–99,999,999 | No floating-point payment amounts; free is explicit |
| Partial unique active attendee/workshop booking | At most one pending/confirmed booking; terminal history retained |
| Pending has expiry/positive amount; paid-price confirmation requires paid=true | Invalid stored combinations rejected |
| Unique Checkout Session and unique event receipt | Stored payment identity and durable webhook replay protection |
| Review unique per attendee/workshop; rating 1–5 | Database-backed review uniqueness/rating bounds |
| Protected financial/user relationships | Referenced owners/attendees and financial records are not silently deleted |

`Resource.file` is a private storage key, not a public URL or database foreign key to the blob table. Heroku policy selects database bytes (maximum 5 MB/file), while ordinary local development retains private filesystem storage. This avoids another paid storage provider, but consumes the application's database quota. Actual local PostgreSQL restart preserved the stored handout bytes. A genuine Heroku web-dyno restart retained the exact uploaded private bytes and authenticated owner access; the temporary handout was then deleted.

## Application architecture

```mermaid
flowchart LR
    Browser[Browser: semantic HTML and CSS] --> Router[Heroku HTTPS router: live]
    Router --> WSGI[Gunicorn and Django]
    WSGI --> Accounts[Accounts and controlled owner roles]
    WSGI --> Domain[Workshop forms, views and transactional services]
    WSGI --> Static[WhiteNoise: collected static manifest]
    Domain --> PG[(SkillSeat PostgreSQL)]
    Domain --> Private[Authorised private attachment response]
    Private --> PG
    Domain --> Stripe[Stripe hosted Checkout: test mode only]
    Stripe --> Webhook[Raw signature validation and idempotent receipt]
    Webhook --> PG
    Scheduler[Heroku scheduler: not configured yet] --> Expire[expire_bookings command]
    Expire --> PG
```

`config` owns environment/release policy; `core` owns the public interface, readiness and response headers; `accounts` owns user/account forms and database-shared abuse limits; `workshops` owns the domain, storage and payment services. Templates are server-rendered without a frontend framework or remote font dependency. The PostgreSQL diagram describes the prepared deployment design; it is not evidence of a completed Heroku release.

Heroku mode must be explicit and rejects missing PostgreSQL/HTTPS origin configuration. Only that mode trusts forwarded protocol, requires database TLS and selects persistent database storage. Local mode remains SQLite by default and distrusts proxy headers. `/health/` performs a read-only database probe and returns generic 200/503 JSON without exposing connection details.

## Routes

| Route | Access / operation |
| --- | --- |
| `/`, `/workshops/`, `/workshops/<id>/` | Public home/upcoming published discovery/detail |
| `/accounts/register/`, `/accounts/login/` | Validated attendee registration/authentication; abuse limited |
| `/accounts/`, `/accounts/edit/`, `/accounts/password/` | Authenticated user's own identity/profile/password |
| `/accounts/logout/` | CSRF-protected POST only |
| `/workshops/<id>/book/` | Authenticated POST; server price and capacity |
| `/workshops/bookings/` | Own history and server payment state |
| `/workshops/bookings/<id>/cancel/`, `.../checkout/` | Own booking, POST only |
| `/workshops/studio/`, `.../new/`, `.../<id>/` | Granted owner permission; own rows, superusers across rows |
| `/workshops/studio/<id>/resources/` | Authorised upload, POST only |
| `/workshops/studio/bookings/<id>/attend/` | Authorised owner records attendance after end, POST only |
| `/workshops/resources/<id>/` | Relevant verified-paid confirmed attendee or authorised owner/superuser |
| `/workshops/resources/<id>/delete/` | Authorised owner, POST only |
| `/workshops/<id>/review/`, `/workshops/reviews/<id>/delete/` | Eligible own review; deletion POST only |
| `/workshops/payments/webhook/` | POST, real Stripe signature/timestamp; sole CSRF exemption |
| `/admin/` | Django staff boundary; financial audit read-only, review moderation superuser-only |
| `/health/` | Public generic read-only readiness probe; no-store |

## Technology stack

| Technology | Actual version/use |
| --- | --- |
| Python / Django | 3.13.16 / 5.2.18, unchanged approved runtime |
| Stripe SDK | 16.0.0, explicitly pinned API 2026-09-30.endive, test mode only |
| Gunicorn / WhiteNoise | 26.2.0 / 6.12.0, actual production WSGI/static serving |
| dj-database-url / Psycopg | 3.1.2 / 3.3.6 with binary driver, PostgreSQL selection |
| PostgreSQL | Heroku 18.4 verified; independent CI on PostgreSQL 17 and 18 |
| SQLite | Preserved local default and regression backend |
| Ruff | 0.17.1, lint/format checks |
| HTML/CSS | Django templates and original responsive CSS |
| JavaScript | Original progressive cancellation confirmation; Node built-in behavioral tests and JSHint 2.13.6 |

`requirements.in` contains deliberate direct pins. `requirements.lock` freezes transitive packages with hashes. Heroku's standard `requirements.txt` delegates to the hash lock with --require-hashes, so default platform installs are reproducible. CI installs the same lock. Optional ignored local CLI/audit tools are not application dependencies.

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

For Heroku set `DJANGO_DEPLOYMENT=heroku`, an attached PostgreSQL `DATABASE_URL`, and `DJANGO_CSRF_TRUSTED_ORIGINS=https://<actual-skillseat-host>`. This explicit mode forces PostgreSQL SSL, trusts the Heroku HTTPS router, and selects database-backed private bytes. Missing production prerequisites fail startup; local development keeps its SQLite/filesystem defaults.

Keys must contain at least 50 characters and five distinct characters; known placeholder prefixes are rejected. Generate a random key rather than merely satisfying those checks. Host values must not contain a URL scheme, port, wildcard, or empty entry. Unknown environment names fail instead of silently choosing a mode. There is no email delivery/verification service. `DATABASE_URL` selects PostgreSQL; proxy trust is enabled only by the explicit Heroku production policy described below. Stripe settings are environment-managed and never printed by application pages.

### Phase 3 local operation

After migrations, `manage.py seed_demo` creates three explicitly fictional workshops with a passwordless demo host (development only, idempotent). It does not create customers, payments or an administrator. Register your own attendee normally. A trusted administrator grants `workshops.add_workshop` through Django admin to provision an approved owner; registration never assigns it. Superusers manage all workshops through the studio and moderate reviews in admin.

Run `manage.py expire_bookings` to release unpaid 35-minute holds. Discovery/reservation/dashboard requests also perform cleanup. No background scheduler is assumed. Private uploads are stored under ignored `private-resources/`, with a 5 MB form limit and authorised attachment responses. Do not expose this folder through a web server. [Stripe setup and policies](docs/phase-3-architecture.md#stripe-test-mode-setup) explain hosted Checkout, signed local forwarding, pending/late events and manual test-refund review.

`requirements.in` retains the approved Django pin; `requirements.txt` is the hash-enforcing Heroku entrypoint. `requirements.lock` additionally freezes its transitive dependencies with hashes and a Windows marker for `tzdata`. `requirements-dev.txt`/`.lock` add only Ruff 0.17.1 for linting and formatting. Install from the lock files for reproducibility. When deliberately updating dependencies, regenerate with `uv pip compile requirements.in --universal --generate-hashes --output-file requirements.lock` and the equivalent command for `requirements-dev.txt`; review and test the resulting diff. Do not change the approved runtime pins incidentally.

## Testing

The original Phase 2 foundation passed **42 tests**: 12 environment contracts, nine Django wiring/database checks, 12 authentication/model boundaries, and nine startup/security checks. All are retained within the current **132 passing Django tests**, independently executed locally and in Windows/PostgreSQL 17/18 CI, plus three JavaScript tests. Real Red/Green runs and the subsequent formatting refactor are recorded in [the evidence log](docs/phase-2-evidence.md). Tests use an isolated in-memory database and real password hashing. Production startup is also exercised in fresh subprocesses.

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

This configuration check does not verify a real TLS endpoint, proxy, production database or hosting platform. Browser, accessibility, capacity, ownership and simulated payment evidence are recorded separately. The genuine hosted Stripe sandbox payment, signed delivery and replay results are recorded in [Phase 3 evidence](docs/phase-3-evidence.md#completed-manual-sandbox-payment--18-october-2026).

Run the custom frontend checks with `node --check core/static/core/actions.js` and `node --test tests/js/confirm.test.cjs`. The three cases verify dismissing cancellation, accepting it, and leaving ordinary/prevented submissions alone. JSHint 2.13.6 checks the browser ES6 source. It initially flagged global strict mode; a function wrapper corrected the finding without disabling the rule. Browser cancellation itself succeeded, but the in-app browser timed out while controlling the native confirmation dialog; a hosted dismissal is not claimed.

### Continuous integration

`.github/workflows/foundation.yml` runs on pushes and pull requests to `main`, and supports manual runs. A Windows runner verifies the official NuGet runtime, creates a fresh environment, installs hash-locked dependencies, asserts exact versions and interpreter location, checks dependency integrity, runs lint/format/system/tests/migrations/production checks, and smoke-tests the server. The checkout action is pinned to an immutable official release commit, permissions are read-only, and no repository secret is required. A random check-only key is generated per run.

[Phase 3 Windows CI run 39159120497](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39159120497) completed successfully on `1d8154bef35d36e29164d1f59b7341fa42a586d4`, including the 110-test suite and separate file-backed concurrency run. The post-payment local run again passed **110 tests plus seven separate concurrency tests**. Completion evidence CI [39164323260](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39164323260) also passed on `2aff9d2932c1ca8d0febab1108c3d38e0efb2d89`; all steps were inspected. These are historical Phase 3 successes. Phase 4 CI results and any pending final-code verification are recorded in the release table below. The earlier real lint failure remains documented; checks were not weakened. CI uses simulated Stripe fixtures and requires no payment secrets. This is verification, not deployment.

## Deployment

SkillSeat is live at **[https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/](https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/)**. The verified app is `skillseat-akkhoujja`, in Europe on heroku-24/Cedar, with an existing Basic web dyno and an existing attached `heroku-postgresql:essential-0` database. PostgreSQL reports **18.4**. The earlier declined-provisioning checkpoint is historical; this continuation independently verified the owner's subsequently successful deployment and reused it without purchasing resources.

The release path is deliberately manual:

1. Run the documented local Django/JavaScript checks, review the diff, commit and push `main`. Inspect all GitHub Actions jobs for that exact revision. CI does not deploy automatically.
2. Use the existing SkillSeat app and its own database attachment. Do not recreate the database or reuse ByteBoard resources. The standard Heroku Python build consumes `.python-version` and the hash-enforcing `requirements.txt` / `requirements.lock`.
3. Privately configure `DJANGO_ENV=production`, `DJANGO_DEBUG=false`, `DJANGO_DEPLOYMENT=heroku`, a strong stable `DJANGO_SECRET_KEY`, the exact `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS=https://skillseat-akkhoujja-e88f42c60993.herokuapp.com`. Heroku supplies the attached `DATABASE_URL`; it must never be printed or committed. Set `PAYMENT_ORIGIN` to that same HTTPS origin.
4. Submit the verified GitHub commit archive through the existing Heroku Build API (source version is the full Git SHA), or deploy the same revision through the existing Heroku Git arrangement. Do not enable unchecked automatic production deployment. Inspect build success and the release result before claiming deployment.
5. The `Procfile` release process runs `python manage.py migrate --noinput`; the web process starts Gunicorn with two workers/two threads. Django migrations preserve records. The build collects manifest static files; WhiteNoise serves hashed CSS, JavaScript and the favicon. Private resource bytes use PostgreSQL, never public static/media storage.
6. Match the released slug's `commit` to the intended SHA, verify the existing `web.1` is up, check `/` and `/health/`, run `check --deploy`, inspect applied migrations and `SHOW server_version`, and review logs without publishing secrets. Verify HTTPS redirects, cookies, CSRF and assets through the public origin.
7. Use temporary fictional records to check hosted workflows, then restart only the existing web dyno to confirm database/private-byte persistence. Clean up only recorded fixture IDs and sessions; never reset the production database.

For Stripe, configure a **test** key privately as `STRIPE_TEST_KEY` and the signing secret of the endpoint `/workshops/payments/webhook/` as `STRIPE_WEBHOOK_SECRET`, using the documented event types in [payment setup](docs/phase-3-architecture.md#stripe-test-mode-setup). Never use live mode. Complete an actual sandbox Checkout and confirm signed fulfillment, duplicate/late/expired rejection and authorised paid download before marking hosted payments verified. **Neither Stripe value is currently configured on Heroku**: Checkout gives clear feedback and the webhook returns 503, rather than granting payment.

`python manage.py expire_bookings` releases expired unpaid holds and prunes expired authentication counters. Discovery/reservation/dashboard requests also perform cleanup. No scheduler is attached; a real scheduled run without HTTP traffic has not been verified. No add-on or extra dyno was provisioned to bypass the user's resource restriction.

The deployed runtime verification is [v19 / `e06fce0`](docs/testing/phase4-live-deployment.json), with no unapplied migrations. The final documentation publication's exact release and SHA are recorded in the delivery response and Heroku release history. Deployment is successful; complete hosted payment/scheduled-expiry verification is still outstanding.

## Security

Environment secrets and local data are ignored. Production retains HTTPS redirects, secure HTTP-only/SameSite cookies, HSTS, frame denial, nosniff and a restrictive application CSP. Only explicit Heroku mode trusts the router protocol. CSRF trusted origins must be explicit HTTPS origins without credentials, wildcards or paths.

Object-level checks scope owners, accounts, bookings, reviews and resources on the server. Forms exclude privileged ownership/payment/visibility fields. Django validates passwords and safe login redirects. Financial admin is read-only. State changes use CSRF-protected POST, except raw signed Stripe webhooks. Test-mode flags, exact server amounts/references, stored Session IDs and unique event receipts protect fulfillment. Cancelled/expired holds never regain seats or resource access from late notifications; administrative test-refund review is explicit.

Authentication abuse controls now use shared database counters keyed by HMAC rather than plaintext IP/username: five failed login attempts per address/username and thirty per address in fifteen minutes; ten registration requests per address/hour. Admin login shares the login controls. Local mode ignores spoofed forwarding headers; explicit Heroku mode uses the router-appended rightmost address. Limits return 429 with Retry-After and no-store, expire naturally and are pruned by the maintenance command. This is a bounded application control, not a complete network DDoS defence.

`pip-audit` 2.10.1 reported **no known vulnerabilities** in the runtime lock on 19 October 2026. Reachable-history/current-source scanning uses credential patterns and exact privately inherited values, prints no secrets and preserves history. A synthetic unit-test DSN was reviewed and classified; no unresolved credential finding remained. These are scoped checks, not proof against every possible unknown vulnerability or secret format.

## Accessibility

WCAG 2.2 AA is the design target. The interface uses semantic landmarks/headings, a skip link, visible focus, explicit labels, associated help/errors, native controls, live status feedback and responsive wrapping. Phase 3's actual browser audit covered five pages at 320, 390, 768 and 1280px: all twenty combinations had one H1/main, no horizontal overflow, duplicate IDs, unlabelled fields, missing description targets or unnamed buttons. Keyboard execution verified skip-to-main and tab focus.

| Selected computed colour pair | Contrast |
| --- | ---: |
| Ink #183c36 / paper #f8f7f2 | 11.26:1 |
| White / teal #145f50 | 7.55:1 |
| Muted #4f625a / paper | 6.07:1 |
| Accent/focus #b8431d / paper | 5.07:1 |

Actual hosted Phase 4 W3C Nu validation returned **no messages** for home, discovery, registration and login HTML after the final runtime changes (transient CSRF values removed before submission). CSS validation returned **valid, zero errors, one system-font vendor-extension warning**. Lighthouse **13.5.0** audited the real public Heroku mobile homepage: **100 performance, 100 accessibility, 100 best practices and 100 SEO**, with no failing accessibility audits; FCP/LCP 0.9s, CLS 0 and total blocking time 0ms in that run. These are point-in-time results, not guarantees or full WCAG certification.

The actual hosted browser checked home, discovery, profile and bookings at **390×844, 768×1024 and 1440×1000**. All twelve combinations had no horizontal overflow, unlabelled form controls or unnamed buttons in the scoped DOM check. Owner/detail/authentication screens were also visually inspected and captured. Navigation wraps on mobile; no hamburger menu is claimed. Keyboard activation of the skip link focused `main-content`; tabbing showed the solid focus outline. Chromium browser emulation is verified; physical devices, Firefox/Safari and screen-reader operation are **NOT VERIFIED**. See `docs/testing/phase4-live-{responsive,lighthouse,html-validation,css-validation}.json` for scoped results. Historical local audits below remain labelled local.

## Limitations

- Current Heroku Stripe test credentials/webhook configuration are absent. Successful hosted payment confirmation, signed rejection/replay/late-event exercises and paid-attendee downloads are **NOT VERIFIED**. The genuine earlier Phase 3 sandbox exercise and deterministic tests do not substitute for the current endpoint.
- There is no attached scheduler. Request-triggered expiration works; scheduled no-traffic hosted execution is **NOT VERIFIED**.
- Temporary production workshops, users, bookings, reviews and handout bytes were removed after evidence collection. Discovery therefore currently shows its honest empty state. Screenshot records are fictional verification fixtures, not advertised real events or real paid attendance. No public administrator or reusable assessment password is shipped.
- The native confirmation prompt exceeded the in-app browser's dialog-control timeout; cancellation succeeded, while hosted dismissal remains unverified. Three deterministic JavaScript tests cover its acceptance/dismissal logic.
- Testing uses Chromium viewport emulation, not physical devices, Firefox/Safari or screen readers. Accessibility coverage is scoped; no full WCAG compliance or institutional grade is claimed.
- No live payments, automatic refunds or email service were introduced. Private files use database quota and are limited to 5 MB each; larger-scale storage, quotas and scanning require further design. Rate limits do not replace network protection.

The supplied Unit 4 criteria and mandatory requirements are now traceable in the assessment matrix. **Phase 4 is still incomplete and not submission-ready**, principally because the current deployment cannot demonstrate the mandatory Stripe payment/content-unlock journey. The supplied final-release requirement also calls for scheduled no-traffic expiration evidence.

## Credits

SkillSeat is a Code Institute Milestone Project 4 repository. Foundation references: [Python's official Windows/NuGet guidance](https://docs.python.org/3.13/using/windows.html#the-nuget-org-packages), [Django's early custom-user guidance](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project), [Django's deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/), [Ruff](https://docs.astral.sh/ruff/), and [GitHub's checkout action](https://github.com/actions/checkout). Project/ASGI/WSGI boilerplate and the initial user migration were generated by Django 5.2.18 and adapted to this configuration.

Phase 3 used [Stripe Checkout creation](https://docs.stripe.com/api/checkout/sessions/create), [Checkout fulfillment](https://docs.stripe.com/checkout/fulfillment), [webhook signature validation](https://docs.stripe.com/webhooks), and the official [stripe-python SDK](https://github.com/stripe/stripe-python). The Stripe best-practices/documentation plugin skills informed the integration; public official documentation was used when the connected documentation tool repeatedly requested authentication. CSS artwork and fictional workshop descriptions are project-created. Screenshots are labelled by provenance: historical local implementation captures and actual hosted production captures. No generated mockups substitute for evidence. Codex assisted implementation, test execution and evidence preparation; project-specific code and CSS artwork are separate from attributed dependencies.

## Reflection

Phase 2 showed why runtime availability must be proved separately from dependency compatibility: the approved versions were compatible, but the bundled uv download list and sandboxed installer prevented installation. Verifying the official NuGet package against its catalog hash provided an isolated runtime without replacing existing installations. Authentication was decided before persistent migrations, and test-first environment/routing/authentication increments preserved evidence of actual failures and fixes. Production checks are useful configuration evidence, but they do not substitute for deployment validation.

Phase 3 made transaction boundaries concrete: independent SQLite connections exposed lock errors that sequential tests could not reveal. Atomic conditional counter updates, rollback and bounded lock retries preserve capacity without claiming SQLite row locking. Signed provider events, rather than redirects, determine payment access; late success deliberately becomes refund review. Browser inspection caught duplicate form IDs that ordinary view tests missed, leading to specific regression tests and semantic shared form rendering. A real CI failure also exposed an unstaged lint fix, reinforcing the need to verify staged content. The separate Red/Green commits and [chronological history](docs/phase-3-commits.md) preserve these actual development steps.


## Booking, payment, resources and reviews — operating policies

```mermaid
stateDiagram-v2
    [*] --> Confirmed: free reservation
    [*] --> Pending: paid reservation / 35 minute seat hold
    Pending --> Confirmed: signed matching paid notification before expiry
    Pending --> Expired: deadline or provider expiry
    Pending --> Cancelled: attendee cancellation or asynchronous failure
    Confirmed --> Cancelled: own cancellation before workshop start
```

Cancellation is available only before workshop start; completed bookings show that deadline rather than an ineligible action. Every active booking consumes one seat. Reservation atomically increments only below capacity, then creates the booking in the same transaction; duplicates/failures roll back the counter. Cancellation/expiry conditionally transition once before decrementing. Capacity edits require reserved <= proposed capacity in the UPDATE. SQLite lock contention and PostgreSQL deadlock/serialization conflicts retry the entire operation within a bounded policy. Real independent connections verified final-seat, duplicate, cancellation, expiry, capacity-edit and payment races on PostgreSQL; no SQLite select_for_update guarantee is assumed.

Paid Checkout snapshots trusted GBP pence, uses stable idempotency and records the Session. Start within four minutes so Stripe's minimum remaining lifetime plus a safety margin fits the 35-minute hold. Redirects only display server state; raw signed, timestamp-validated, test-mode events with matching Session, amount, currency and reference grant payment. Duplicate receipts are no-ops. Unpaid/failed/expired events cannot grant resources. Late or mismatched success sets refund review without restoring a seat; the operator reconciles the test Dashboard and arranges any appropriate test refund manually. No live or automatic refunds are made.

Only an authorised owner/superuser or a relevant paid+confirmed attendee can download a private attachment. No public media route is registered. Cancellation, expiry or unpaid/unrelated identity revokes access. Reviews require confirmation, workshop end and explicit host-recorded attendance; trimmed bodies are 10–2000 characters, ratings 1–5, one own review per workshop. Superusers control visibility; editing a hidden review does not republish it.

## Release verification and assessment readiness

| Executed check, 19 October 2026 | Actual result and scope |
| --- | --- |
| Final runtime source / verification release | `e06fce0a855a650afd75469ffcd089a1469813b2` / Heroku v19, succeeded |
| Local full Django suite | **132 passed, 25.619s**; original foundation tests retained |
| Windows CI | **132 passed, 6.023s**; separate seven file-backed races passed, 0.323s |
| PostgreSQL 17 CI | **132 passed, 6.830s**, including seven independent-connection races; Gunicorn smoke passed |
| PostgreSQL 18 CI | **132 passed, 8.966s**, including seven independent-connection races; Gunicorn smoke passed |
| Custom frontend JavaScript | Three behavior tests, Node syntax check and JSHint 2.13.6 pass; native browser dismissal limitation documented |
| CI | [All three runtime jobs succeeded](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39324116798); exact run/job results in `docs/testing/phase4-live-ci.json` |
| Hosted core journeys | Real HTTP/CSRF/DB effects, concurrent final-seat booking, owner/review/resource CRUD, negative permissions and actual restart persistence verified |
| Production policy / migrations / database | `check --deploy` passes; no unapplied migrations; actual PostgreSQL **18.4** |
| Static assets / logs | Hashed CSS/JS served; immutable CSS cache policy; no traceback or Heroku H-code in inspected log window |
| HTML / CSS | Four hosted public pages: no W3C Nu messages; CSS: zero errors, one font warning |
| Lighthouse | Actual hosted mobile: **100 / 100 / 100 / 100**; no failing accessibility audits |
| Responsive / keyboard | Twelve hosted viewport/page combinations without horizontal overflow; skip navigation and visible focus verified |
| Fixture cleanup | Exact fictional rows/private bytes removed; application counts return to baseline; throttle counters preserved |
| Unit 4 audit | Supplied actual criteria **1.1–5.6**, **M(i)–M(vii)** and mandatory requirements 1–13 mapped to implementation, tests, evidence and status |
| Outstanding assessment requirement | **Mandatory 6 / criteria 4.1–4.2 PARTIAL:** current hosted Stripe payment and content unlock unavailable |
| Outstanding release requirement | Scheduled no-traffic expiration **NOT VERIFIED**; no new service authorised |

The [assessment matrix](docs/assessment-audit.md) uses **PASS / PARTIAL / FAIL / NOT VERIFIED** as evidence statuses, not an awarded grade. It records the supplied Unit 4 document by filename, printed pages and SHA-256, and separately maps the user's 13 mandatory requirements. The main README follows ByteBoard's presentation standard with purpose, original planning provenance, inline production images, schema/architecture/workflow diagrams, operating policies, deployment and actual test results. ByteBoard was read only.

## Licensing status

No repository-wide licence has been granted. Public availability does not itself grant reuse rights. Django-generated boilerplate and third-party dependencies retain their own licences; the credits identify the official sources and tools. Choosing a licence remains the repository owner's decision and is not presented as an assessment pass.

The [Phase 4 checkpoint report](docs/phase-4-release-report.md) consolidates actual release results, the complete implementation-commit chronology and precise continuation steps. The substantive design, model, role, state and verification evidence remains presented directly above.
