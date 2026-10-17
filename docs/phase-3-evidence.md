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
