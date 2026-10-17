# Phase 3 development evidence

Baseline: `9b165941b3a35123409e43b85b991935b29a39f9`, clean tree, fetched origin with 0/0 divergence. The unchanged foundation suite passed all 42 tests on 17 October 2026.

## Architecture decisions before implementation

One `workshops` app owns Workshop, Booking, PaymentAttempt, PaymentEvent, Resource and Review. All user foreign keys use AUTH_USER_MODEL. Administrator-granted `workshops.add_workshop` permits ownership; superusers manage across owners. Registration never assigns permissions.

Capacity uses an atomic conditional UPDATE of Workshop.reserved followed by booking creation in the same transaction. A database check enforces 0 <= reserved <= capacity; a partial unique constraint prevents duplicate pending/confirmed bookings. The first database operation in mutating transactions is a write, avoiding SQLite read-to-write lock upgrades. Capacity edits use conditional updates too. Independent connections will test races; PostgreSQL remains untested.

Money is integer GBP pence. Dates are aware UTC. Paid bookings hold a seat for 35 minutes; Checkout expires at the same deadline (Stripe requires at least 30 minutes). Expiry is executed during booking and by `expire_bookings`. Only signed test-mode payment events with matching stored session, amount and currency can confirm. Late payments require administrative refund review and never regain a seat automatically.

Reviews require a confirmed booking, ended workshop and owner-recorded attendance. Resources are private file responses after object-level authorization; no public media route.

## Planning evidence

The [journey wireframes](design/phase-3-wireframes.md) were created before business interfaces. Final captures and differences will be recorded separately.

## Verification log

- Baseline: `manage.py test -v 1`: 42 tests passed; system checks clear.
- Implementation and verification are ongoing. No Phase 3 completion claim yet.

### First development slices

- Discovery Red: missing `workshops` module. Green: 5 tests passed for visibility, missing IDs, dates, price and database capacity checks.
- Account Red: all 5 new tests failed with missing routes. Green: 17 account tests passed (new and foundation), covering password hashing, privilege forgery, own-profile editing and password-change session continuity.
- Booking Red: missing Booking model. Green: 6 lifecycle tests passed, including repeated cancellation and expiry release.
- Owner/concurrency Red: 5 missing-route failures and 3 real SQLite lock errors. Green: all 9 passed after owner-scoped management and bounded whole-operation lock retries. Races use two threads, a barrier and independent Django connections; no mocked database locking.
- Important finding: shared-memory SQLite raises immediate table-lock errors rather than waiting like file-backed SQLite. Retries are bounded; exhaustion returns a validation error and never bypasses capacity checks. Production PostgreSQL concurrency has not been tested.
- First integrated checkpoint: 67 tests passed, no migration drift, Ruff lint and format clear. Pushed through `611242b`.
- Resource/review Red: missing Resource model. Implementation then exposed missing public review rendering; fixed template before Green. All 6 tests passed with real temporary-file delivery. Restricted Windows temp access required an approved unsandboxed test invocation.
- Stripe connector returned repeated authentication requests; official public Checkout creation, fulfillment, signature and stripe-python documentation were read instead. No STRIPE environment credentials were present. PyPI reported stable stripe-python 16.0.0; using that verified release rather than the older version listed by the bundled skill.
- Payment Red: missing PaymentAttempt model. Green: all 10 payment tests passed, including real SDK HMAC signature validation over a simulated payload, duplicate event receipts, async success, tampered amount/currency/reference, test-mode enforcement, late success and reordered expiry. API initiation is mocked; this is not evidence of an actual Stripe transaction. SDK 16 reports API version `2026-09-30.endive`, pinned explicitly.
- Real CI run [39054102680](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39054102680) failed lint: the local unused-import correction had not been staged. `c707337` records the fix; the failing result is retained honestly.
- Interface Red: missing discovery links and shared styling. Green: 11 interface/foundation tests passed. The existing foundation home assertion was updated from the obsolete Phase 2 planning sentence to the functional discovery link; all original 42 test cases remain, with no deleted tests.
- Security audit: 9 tests found missing private cache headers; added no-store on authenticated responses and a restrictive CSP. Full checkpoint: 94 tests passed in 15.544s, no migration drift.
- Expanded concurrency: 13 owner/race tests passed on shared-memory SQLite; all 7 races passed on file-backed SQLite in 2.257s. Covered final seat, duplicate reservation, cancellation, expiry, capacity reduction, duplicate payment receipt and payment-vs-cancellation. Each worker opens its own connection and synchronises at a barrier. No PostgreSQL claim.
- Demo-data Red: missing seed command. Green: idempotent command test passed; 3 fictional workshops created locally, no login passwords or real customers.
- Integrated checkpoint: 99 tests passed in 15.408s, lint/format/whitespace checks clear. Pushed through `187871d`.
- Browser found duplicated `id_title` attributes in the workshop/resource forms and offered booking/review actions before eligibility. Added two failing regression tests, then separate resource field IDs and eligibility-aware controls; all 4 interface tests passed.
- Stripe CLI 1.54.0 installed into ignored `.local-tools` using the official npm package. Isolated `sandbox create --non-interactive` failed with `email is required`; no user email or Git identity was transmitted. No test keys or signing secret have been created. This is the remaining external integration verification dependency.

## Final local implementation audit

- Exact assertions passed: Python 3.13.16, Django 5.2.18, Stripe SDK 16.0.0. `uv pip check --python .venv/Scripts/python.exe`: all 12 installed packages compatible. Stripe and transitive packages were installed with the regenerated hash lock.
- Ruff lint and format checks passed. `manage.py check`: no issues.
- Initial final audit: 109 tests passed in 17.242s. A subsequent discovery edge-case test exposed past-workshop seat advertising (Red), corrected by upcoming discovery filtering and closed past details (Green: all 7 workshop tests). Final `manage.py test -v 2`: **110 tests passed in 17.209s**. [Genuine full output](testing/phase3-tests.txt) includes authentication, account isolation, public visibility, ownership, booking lifecycle/capacity, payment failure/signatures/replay, private-file delivery/deletion, review eligibility/moderation, interface and connection races.
- Separate final file-backed SQLite run: **7 tests passed in 2.386s**. [Genuine full output](testing/phase3-file-concurrency.txt). No PostgreSQL execution is claimed.
- Five incremental workshops migrations applied locally; fresh test databases also apply all five. `makemigrations --check --dry-run`: no changes. `migrate --check`: successful.
- `expire_bookings`: executed successfully, 0 expired holds at audit time (expiry release is exercised in tests). No scheduler assumed.
- `scripts/smoke_server.py`: real development server HTTP 200 and SkillSeat home verified; child stopped by script.
- Production `check --deploy --fail-level WARNING`: no issues, with explicit check-only allowed host, strong transient key, debug false and no silenced checks. This is configuration verification, not deployment.
- Actual browser registration/login/free booking/cancellation/paid-pending/unconfigured-payment/owner-creation/logout journeys executed. [Design verification](design/phase-3-verification.md) preserves captures and the 20-combination responsive DOM audit. Temporary fictional test login disabled and its owner permission revoked afterward.
- Semantic form Red: missing block password help; Green: 22 interface/account tests passed. Price Red: three invalid prices were accepted; Green: 12 model/ownership tests passed after validation and migration. Existing-booking Red: missing management action; Green: 12 booking/interface tests passed. Final negative security audit: all 18 resource/regression tests passed.

## CI and repository state

- [39055816793](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39055816793): successful Windows run at `187871df0d295c464d9c33f0aa9e1414b10119e2`, 99 tests at that checkpoint, file-backed races, exact versions, hash installation, lint/format, migrations, expiry, production checks and real-server smoke.
- [39057049274](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39057049274): successful Windows run at `c71bc8dcd10e296807f72248c0d5a706f4e76b57`; every job step inspected and successful, including the then-current 109 tests, file-backed races, hash installation, migrations, expiry, production checks and real-server smoke.
- Live origin/main and local HEAD were both `c71bc8dcd10e296807f72248c0d5a706f4e76b57` with a clean tracked/untracked tree before the final past-workshop regression. Final delivery reports the subsequent actual CI run, live SHA comparison and clean tree; a dispatched run alone is never treated as success.
- Local Markdown file links checked successfully. A scoped tracked-file payment-credential pattern scan found no matching credentials. This is not a comprehensive historical secret scan; Phase 4 retains that release responsibility.
- [Chronological commit evidence](phase-3-commits.md) lists full SHAs and accurate titles. Separate Red-stage commits stayed local until the paired implementation restored checks.

## Remaining external dependency and continuation

Phase 3 is **implemented and locally verified, but not fully complete** until a genuine Stripe sandbox Checkout/payment/signed-webhook exercise succeeds. Automated initiation is mocked; synthetic provider payloads use the real SDK signature validator. No real Stripe transaction is claimed.

The only required human intervention is dedicated Stripe sandbox/test access: set a restricted test key privately in the execution environment, or explicitly authorise an email identity for the official CLI's claimable sandbox provisioning. Do not paste keys into Git or project documentation. The CLI is already available in ignored `.local-tools/node_modules/.bin/stripe.cmd`. No sandbox was created and no user identity sent.

Resume by checking HEAD/status and the latest successful CI, then follow the Stripe setup steps in phase-3-architecture.md: start CLI forwarding to loopback, export its signing secret privately, restart Django, reserve a paid fictional workshop, complete test-mode hosted Checkout, verify stored matching paid state/private resource access and replay behaviour using actual provider evidence. Record the genuine result, rerun relevant/full checks, commit/push the evidence, and verify final CI/remote/tree. Keep test-only mode. The fictional browser user's password is unusable; create a fresh disposable attendee or use normal registration.

Phase 4 has not begun. Production deployment, database/proxy/storage/scheduler selection, broader accessibility/release validation and final project reflection remain Phase 4 work after the Phase 3 external gap is resolved.
