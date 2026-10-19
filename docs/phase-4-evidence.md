# Phase 4 — release and assessment evidence

## Baseline and scope — 19 October 2026

Started at `bb0d7cec2c5eace63515fead3939f7e1a8a6f0fe`, clean working tree. The supplied baseline matches HEAD. The unchanged suite passed **110 tests in 12.673s**. Phase 3's genuine sandbox payment and signed webhook record is preserved.

The user authorises a separate SkillSeat Heroku app in the existing ByteBoard account, subject to explicit cost approval before new billable resources. ByteBoard's public README was read as a presentation/deployment reference; its application, credentials and database were not modified or reused.

## Release plan before implementation

- Retain Python 3.13.16, Django 5.2.18, Windows CI and local SQLite. Add explicitly configured PostgreSQL, WhiteNoise and Gunicorn for Heroku. Never fall back to SQLite on a dyno.
- Store private resource bytes in the application's own PostgreSQL database (5 MB maximum per file), avoiding ephemeral dyno uploads and an extra billable storage provider. Existing local file storage remains available outside Heroku. This small assessed application accepts the database-size tradeoff; storage remains private and downloads retain server-side authorisation.
- Keep `expire_bookings` as the idempotent scheduled command. A Heroku schedule and actual execution must be verified after account/billing access, not inferred from code.
- Verify actual PostgreSQL connections and races independently of SQLite; fix transaction retry/ordering defects exposed by real PostgreSQL.
- Improve authentication abuse controls, error pages, health checking and operational logging with regression tests.
- Present diagrams, original planning artefacts and actual screenshots directly in README. Newly rendered diagrams of old structured planning are labelled as Phase 4 renderings, never historical image wireframes.

## External access observations

- Heroku CLI was initially absent; no HEROKU_API_KEY or netrc authentication was found. Official CLI installation is being prepared in ignored `.local-tools`.
- Stripe Directory plugin installed, but its Heroku search returned `Invalid user agent`; official Heroku documentation is used as the fallback. No provider account or resource was provisioned through Directory.
- Authenticated GitHub API access returned rate-limit HTTP 403. The requested ByteBoard README was retrieved from its public raw GitHub URL instead. No rate limit was bypassed with alternate credentials.
- Public Code Institute course pages describe four milestone projects and the Django module. The learner-specific authoritative MS4 rubric/submission instructions have not yet been located. Student repositories and marketing pages are not treated as a rubric.

Implementation, release and assessment checks are ongoing. Heroku deployment is not yet claimed.
