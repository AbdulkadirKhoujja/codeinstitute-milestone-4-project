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

## Implemented Red/Green release slices

- Release configuration Red: missing config.release module. Green: 6 policy tests pass, including no dyno SQLite fallback, explicit HTTPS origins, safe configuration representation and production database TLS enforcement.
- Persistent storage Red: missing PrivateResourceBlob. Green: 2 storage tests pass for new-instance persistence, exact bytes, no public URL, deletion, missing files and 5 MB bounds; existing filesystem behaviour retained.
- Production dependency inputs now live in requirements.in; requirements.txt is the hash-enforcing standard Heroku entrypoint. Gunicorn 26.2.0, WhiteNoise 6.12.0, dj-database-url 3.1.2 and Psycopg 3.3.6 are deliberately pinned; existing Python/Django pins unchanged.
- PostgreSQL retry Red: a simulated serialization conflict escaped. Green: whole-operation retry handles 40001/40P01; unrelated operational errors still propagate. This unit test is separate from the actual engine execution below.
- Readiness/error Red: missing endpoint and generic framework 404. Green: generic no-store database readiness and branded safe error pages; all 12 readiness/security tests passed.
- Authentication-abuse Red: missing persistent counter. Green: 19 account/throttle tests passed. Limits are shared in the DB, expire naturally, reject local spoofed forwarding and do not store plaintext identities. Admin login uses the same guard.

## Actual local PostgreSQL execution

GitHub's new Windows/PostgreSQL jobs were queued, so a separate local engine was verified independently. PostgreSQL's official Windows download page links EDB's binary archives. Its current 17.11 Windows x64 archive resolved to `https://get.enterprisedb.com/postgresql/postgresql-17.11-5-windows-x64-binaries.zip`. Download size: 381531864 bytes; observed SHA-256: `80379b2c04d51c30225532e0ae04509899141e9957ed096fe749d7fd9df8f82f`. This observed hash records the downloaded artefact; it is not claimed to be an independently published vendor checksum.

Only bin/lib/share were safely extracted into ignored .local-tools. A new password-protected cluster was initialised there and bound to 127.0.0.1:55432, without a Windows service or changes to another database. Credentials were generated privately and not printed/committed. Actual server query reported **PostgreSQL 17.11 on x86_64-windows**.

- **125 tests passed in 28.174s** on the actual PostgreSQL server, including all seven barrier-synchronised independent-connection races. [Raw output](testing/phase4-postgres-tests.txt).
- All migrations, including accounts/0002 and workshops/0006, applied to the disposable database.
- A private handout was saved through the database backend; the actual PostgreSQL server was stopped and restarted. A fresh application process read identical bytes, then deleted the probe.
- A pending fictional hold was expired before restart; after restart `expire_bookings` ran without HTTP traffic and released exactly one place. This verifies the executable command, not a configured Heroku schedule.
- [Sanitised operation result](testing/phase4-postgres-operations.json). Heroku database/SSL, app restart and hosted persistence are not yet verified.

## Security and documentation audits

- pip-audit 2.10.1 reported **no known vulnerabilities** in the runtime lock; [actual JSON](testing/phase4-dependency-audit.json). This is point-in-time advisory coverage.
- The reachable-blob scan initially flagged a new documented synthetic unit-test PostgreSQL URL. Its source was reviewed and explicitly classified; no credential value was printed. The subsequent 261-blob run had no unresolved pattern findings and no broken Markdown file targets. The script also checks exact privately inherited credential values without printing them. [Actual scoped audit](testing/phase4-source-audit.json).
- README now embeds the genuine planning source renderings, real local screenshots, ERD, architecture/state diagrams, substantive role/state/storage/deployment explanations and actual results. Original planning provenance is explicit: no original mobile image wireframe existed; SVGs are dated Phase 4 renderings of the unchanged 17 October text.
- [Assessment matrix](assessment-audit.md) labels Pass/Partial/Fail/Not Verified and does not invent institutional criterion IDs. The actual learner-specific rubric remains requested and unavailable.

## Account and billing checkpoint

Official Heroku CLI **11.12.0** is installed locally; `auth:whoami` reports **not logged in**. A request to authenticate the existing ByteBoard account is pending. Public Heroku pricing on 19 October lists Basic at USD 7/month and Postgres Essential-0 at USD 5/month; these are provisional public prices, not an approved purchase or verified account offer. Scheduler dyno usage and actual account eligibility must be checked before a concrete exact-cost approval. No Heroku app/add-on/paid plan has been created or changed.
