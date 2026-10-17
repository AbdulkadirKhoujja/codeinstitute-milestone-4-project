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
