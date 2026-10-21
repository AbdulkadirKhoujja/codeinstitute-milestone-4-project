# Phase 4 — release and assessment evidence

**Final checkpoint, 21 October 2026: Phase 4 complete within supplied project scope; hosted Stripe commerce and unattended expiry/restart recovery verified. Ready for assessment submission, with optional coverage/operational limits stated.** The chronological notes below preserve earlier observations; the final hosted continuation section and updated release report supersede their old empty-app and unavailable-rubric statements.

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

At the initial checkpoint, official Heroku CLI **11.12.0** was installed locally and `auth:whoami` reported **not logged in**. The user subsequently authenticated; the later verified inventory and explicit billing decision are recorded below. Public Heroku pricing on 19 October lists Basic at USD 7/month and Postgres Essential-0 at USD 5/month; these are provisional public prices, not an approved purchase or verified account offer. Scheduler dyno usage and actual account eligibility must be checked before a concrete exact-cost approval. No Heroku app/add-on/paid plan has been created or changed.

## Final local release checks and actual interface findings

- Final suite after both browser findings were corrected: **127 SQLite tests passed in 26.487s; 127 PostgreSQL tests passed in 35.306s**, with seven actual independent-connection races in each full run. Separate file-backed SQLite race run: **7 passed in 0.667s**. Raw outputs are in testing/phase4-{sqlite-tests,postgres-tests,sqlite-races}.txt.
- Exact Python 3.13.16 / Django 5.2.18 assertions, uv dependency consistency, Ruff lint/format, Django deployment checks, migration drift/applied checks and static manifest collection passed. The uv-created local environment has no pip module; dependency integrity was correctly checked using the established uv pip check, rather than reporting the unsuccessful pip invocation as a pass.
- Original Lighthouse 13.5.0 run reported standard category scores of 100 but an additional accessible-name mismatch. Test 6ec7296 genuinely failed before fix 716f73f; interface tests then passed. Restarting the no-reload local server was necessary before a valid rerun. Final actual mobile homepage audit has all four standard scores 100 and no failing accessibility audits. Before/after scoped JSON retained; these are local, not Heroku scores.
- W3C Nu returned no messages for home/discovery/registration/login HTML; transient CSRF values removed before submitting public page markup. CSS POST was refused, then documented GET returned valid/0 errors/1 system-font vendor-extension warning. Actual JSON retained; no fabricated validator result.
- Actual owner browser login, attendance recording, exact protected handout download, attendee review creation after that attendance, unpaid direct-file 404 and branded safe 404 with debug disabled were exercised. The completed workshop/users/review are explicitly fictional local fixtures. Screenshot captions never imply a real event or payment.
- The completed-workshop dashboard still offered cancellation even though the server denied it. Test 2c41a9f captured Red; c31e504 now shows the deadline and 14 interface/booking tests passed. Final full suites above include it.
- Owner/review pages checked at 390px: document 375px, no horizontal overflow; actual resource/review keyboard focus captured. No physical-device, screen-reader or full WCAG claim.
- Actual GitHub README inspection at a3cf413 found all 11 embedded original images loaded with nonzero natural widths; ERD, architecture and booking-state Mermaid diagrams all rendered. Expanded release screenshots are directly embedded in README. Further final render checks will be recorded after pushing.
- CI now also runs the actual two-worker/two-thread Gunicorn process on Linux; Windows development-server smoke passed locally. Gunicorn cannot execute natively on Windows and its Linux CI result remains unverified until the queued runner completes.

## Authenticated Heroku inventory and explicit billing decision

The user completed existing-account login. CLI identity and app inventory confirm ByteBoard ownership. Read-only baseline: byteboard-app ID 1883b6b1-ab49-4fba-8956-ba41b26243af, release v18, one Basic web dyno and its own Essential-0 add-on. No ByteBoard configuration, process, database or attachment was modified. A private HMAC baseline of its configuration was saved without printing or copying secrets into evidence.

A separate **empty, non-running app record** was created: skillseat-akkhoujja, ID d49ce190-95dc-42a8-a0d8-34f6e38def7e, Europe, Cedar/heroku-24. Assigned hostname skillseat-akkhoujja-e88f42c60993.herokuapp.com is **not an application deployment**. Actual inventory confirms zero formation entries and zero add-ons. Its actual available dyno catalog includes Basic at USD7/month. Actual Essential-0 catalog is USD5/month; Scheduler Standard is USD0/month plus billable one-off dyno runtime. Private database storage needs no storage add-on.

The concrete proposal was USD12/month base with Basic scheduler/verification runtime billed per second (approximately USD0.01/hour), within a USD20/month pre-tax ceiling. The user explicitly answered **Do not provision paid resources**. No billable resource was created; no paid plan, database, scheduler or deployment was attempted. This is an unavoidable authorisation boundary, not a technical permission to work around. Full hosted HTTPS, migrations/storage/restart, scheduled no-traffic expiry and endpoint/payment journeys remain blocked. Reuse this app record if the owner later gives explicit new cost approval; do not create duplicate app records.

The actual learner-specific assessment rubric/submission instructions are still unavailable. The requirements matrix remains clearly best-effort, with no invented institutional identifiers or grade prediction. Phase 4 remains incomplete and not submission-ready until mandatory hosted and authoritative assessment evidence exists.

## Final preservation and handoff checks

- Read-only final Heroku comparison: ByteBoard configuration HMAC unchanged, latest release18, same Basic formation and original add-on ID; public homepage HTTP 200. SkillSeat formation/add-ons remain empty. [Actual sanitized comparison](testing/phase4-heroku-preservation.json).
- Expanded README actual GitHub inspection after d0241c4: **all16 embedded images loaded**, including release account/resource/review/error captures. The original three Mermaid renders were verified separately and not changed. [Rendered image observations](testing/phase4-readme-render.json).
- Earlier Phase 4 CI [39280184246](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39280184246) completed successfully on8f18b0c; Windows/PostgreSQL steps inspected. Latest-code CI [39284481374](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39284481374) remains separately monitored; a queued run is not a success.
- Only the fictional release fixture accounts were disabled and their workshop unpublished; retained Phase 3 sandbox financial records were not modified. The task-created local server and disposable PostgreSQL cluster were stopped gracefully, with local data preserved.
- [Consolidated release report and full SHA chronology](phase-4-release-report.md). The final delivery identifies its own documentation commit and synchronized remote SHA without creating a self-referential commit hash in this file.

## Final hosted continuation — 19 October 2026

Independently confirmed deployed v16/b546e49 with existing Basic/PostgreSQL 18.4 and no unapplied migrations. The earlier empty-app checkpoint is historical. Reused the existing app/resources without provisioning services or modifying ByteBoard. Full details, actual SHA chronology, release/CI links and remaining blockers are in [the updated release report](phase-4-release-report.md).

Three genuine Red/Green slices corrected discovery filtering, authenticated login/registration access (actual supplied Unit 4 criterion3.2), and absent custom JavaScript (supplied mandatory requirement8). Final runtime e06fce0/v19 passed132 Django tests on Windows/PG17/PG18, three JavaScript behavior tests and JSHint. Actual hosted workflows, final-seat concurrency, own CRUD, authorisation/CSRF, request expiry, throttle and genuine restart/private-byte persistence were exercised. Exact fictional rows/files/sessions were cleaned up; no production database reset.

Actual hosted W3C HTML four pages returned no messages; CSS valid/0 errors/1 font warning. Hosted mobile Lighthouse 13.5.0 returned 100 in all four standard categories. Twelve viewport/page combinations had no horizontal overflow or unlabelled controls; skip-to-main and visible focus worked.22 actual hosted JPEG captures are embedded in README, with header-derived dimensions/hashes in their manifest. Prior local evidence/wireframe provenance is retained. No full WCAG, physical-device or screen-reader claim.

The learner supplied the actual Unit 4 F/650/3528 PDF (printed 55–65) and13 mandatory requirements; [assessment matrix](assessment-audit.md) now uses their real IDs. Hosted payment/content unlock remains PARTIAL because Stripe settings are absent; the endpoint returns503 rather than trusting a forged event. No scheduler is attached, so no-traffic hosted expiration remains NOT VERIFIED. Native confirm-dialog automation timed out; actual cancellation succeeded, dismissal is covered by JS tests but not independently verified in the hosted browser. These are explicit limitations, not fabricated passes.

All final publication checks must complete before delivery; the exact documentation commit, final release and CI URL are reported there. No fifth phase, extra billable resource or artificial commit was created.

Actual post-push GitHub inspection at `8cdfb74`: all **38 inline images** loaded with nonzero natural widths, including every one of the **22 production captures**; all **three Mermaid diagrams** rendered with their expected labels. The existing `testing/phase4-readme-render.json` now records this current check.

## Hosted Stripe continuation — 21 October 2026

[Detailed current commerce report](phase-4-hosted-stripe.md) and [sanitised assertions](testing/phase4-hosted-stripe.json) supersede the historical missing-credentials gap above. Heroku v22 on source `3d28b6858c72132b1d86a93aba8822aaa429c595` completed the genuine £1 sandbox purchase, direct signed fulfillment, two provider resends, provider expiry and exact paid handout download. Mandatory6 / criteria4.1–4.2 now PASS in the executed scope. The user approved the missing test endpoint/private signing-secret configuration and manually submitted both test-card cases. Secrets were not printed or committed. Cleanup retained sandbox financial audit records, disabled the three fictional users, unpublished the workshop, removed five fixture sessions and removed the handout/private bytes. No scheduler or extra service was provisioned.

## Phase 4 completion — 21 October 2026

The v22 payment evidence was committed/pushed as `03e7821` and all three CI jobs succeeded. Scheduler Red `ddc9afc` had five genuine errors before implementation; Green `8aeb4e2` passed 137 tests locally and on Windows/PG17/PG18. The existing web workers now run the existing `expire_bookings` command independently of traffic, without new resources. Actual hosted periodic expiry and restart recovery passed with zero router requests in the observation window; the future control hold and all pre-existing sandbox financial audit records were preserved. Exact scheduling fixtures were removed. [Completion report](phase-4-completion.md), [execution evidence](testing/phase4-unattended-expiry.json), [CI](testing/phase4-completion-ci.json). Historical open/blocked checkpoints above are superseded, not relabelled as completed executions.
