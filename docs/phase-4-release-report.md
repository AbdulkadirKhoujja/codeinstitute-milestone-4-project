# Phase 4 release and submission-readiness report

19 October 2026. **Incomplete: required hosted release is blocked by explicitly declined paid provisioning.** No fifth phase is proposed. The core Phase 3 application and its genuine sandbox-payment evidence are retained. Independent release engineering and available local checks are complete at this checkpoint.

| Delivery requirement | Actual result |
| --- | --- |
| Working live SkillSeat URL | None. Assigned empty-app hostname skillseat-akkhoujja-e88f42c60993.herokuapp.com is not a deployed application |
| Heroku account and ByteBoard | Existing account authenticated; ownership verified. ByteBoard release v18, Basic web dyno, original Essential-0 attachment and private config fingerprint unchanged. Public HTTP200 |
| Separate app | skillseat-akkhoujja, d49ce190-95dc-42a8-a0d8-34f6e38def7e, EU, Cedar/heroku-24; zero dynos/add-ons |
| Billing | Actual Basic USD7/month, Essential-0 USD5/month, Scheduler USD0/month plus job runtime. User declined proposed USD12 base / USD20 total pre-tax ceiling. No paid resources provisioned |
| Production engineering | Explicit Heroku PostgreSQL/TLS/proxy/origin policy; Gunicorn Procfile release/web; WhiteNoise manifest static; startup fail-closed; safe readiness/errors; database-shared HMAC auth limits |
| Private storage | Heroku mode stores max5MB private bytes in the application's PostgreSQL, never public media. Actual local PostgreSQL restart retained exact bytes. Hosted persistence unverified |
| Expiration | Idempotent command released one expired hold without HTTP traffic after actual local PG restart. Scheduler not provisioned or configured; recurring execution unverified |
| Hosted user journeys | None claimed; blocked. Existing Phase 3 provider exercise remains genuine sandbox evidence, not a Heroku deployment |
| Local browser journeys | Owner sign-in/attendance, exact protected owner download, eligible fictional review, unpaid file denial, debug-disabled error page; responsive/keyboard evidence saved |
| SQLite full suite | 127 passed, 26.487s; original foundation/core cases retained |
| PostgreSQL full suite | 127 passed, 35.306s, actual PostgreSQL17.11; seven barrier/independent-connection races included |
| Separate SQLite file-backed races | 7 passed, 0.667s |
| Versions/migrations/static | Python3.13.16/Django5.2.18 asserted; no migration drift/unapplied local migrations; new accounts0002/workshops0006 applied; production static collection129 assets/387 processing outputs |
| Quality/configuration | Ruff lint/format, uv dependency consistency, Django system/deployment checks, real local server smoke and whitespace passed |
| Security | Existing permissions/payment/replay/CSRF/resource tests retained; shared abuse controls and production policy added. pip-audit2.10.1: no known runtime advisories. Scoped source/history scan: no unresolved credential findings; no history rewriting |
| Formal validation | W3C Nu four anonymous pages: no messages; W3C CSS valid/0 errors/1 system-font extension warning. First CSS POST refusal recorded; GET succeeded |
| Lighthouse | 13.5.0 local mobile homepage:100 performance/accessibility/best practices/SEO. Additional brand audit finding corrected through genuine Red/Green; rerun no failed accessibility audits |
| README visuals |16 actual embedded images loaded on GitHub; three Mermaid diagrams rendered; original text provenance and dated SVG renderings explicit. No invented historical/mobile wireframe or hosted screenshot |
| Assessment coverage |[Requirements matrix](assessment-audit.md) uses supplied scope and available official context. Authoritative learner-specific MS4 brief/rubric/submission source still missing; no institutional grade/compliance claim |
| Licensing |No repository-wide licence granted; official dependencies/source/tool credits recorded; owner retains licensing decision |
| CI |[Earlier Windows and PostgreSQL run39280184246](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39280184246) succeeded on8f18b0c; all steps inspected. [Latest-code run39284481374](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39284481374) was queued at inspection. New Linux Gunicorn smoke is not yet claimed passed |

## Genuine engineering corrections

Tests preceded release-policy, database-storage, PostgreSQL retry, readiness/error and shared-throttle behavior. Actual browser/Lighthouse findings also produced separate genuine Red/Green commits: brand accessible-name mismatch and cancellation offered after workshop start. No tests were removed or weakened. Full raw test results, before/after Lighthouse details, validation JSON, actual browser observations and sanitized Heroku inventory/preservation evidence are under `docs/testing/phase4-*`.

## Chronological Phase 4 commits through this report checkpoint

The report's own documentation commit and final synchronized SHA are identified in the delivery response. The following full hashes are actual committed history, not planned commits:

```text
49802e700dea527f8fd484a17b929721d699bace docs: establish Phase 4 release plan and verified baseline
334268c9c6cbb1e65eb242485803b69a3beb27e3 test: define explicit Heroku PostgreSQL and proxy policy
2297f66a0a7f1a09cabc8d2c568be228506a3863 feat: configure explicit PostgreSQL Heroku runtime and static serving
33a381996205a7ec8839efc9a238def51d4c8538 test: require persistent private resource storage across instances
07a650e9c13d14b8e58e50ca4e05b6d11325d5df feat: persist authorised private resource bytes in the application database
0ab176c767973993d0b3ee0c66f4b50d8a58addf build: make Heroku default installs enforce the runtime hash lock
abb70d57ad052694115b9a8a8dee53115fe8bbf6 test: exercise PostgreSQL serialization retry policy
2da387a604c2528d7edb879e684dade2b8ecbaac ci: verify PostgreSQL transactions while preserving Windows SQLite coverage
ecf045299f6fd95ea8ca7fe3198570d18e8e9a45 test: define safe readiness and helpful release error responses
8f18b0cc6d48b75904ef8f4c725f0f0fe181386b feat: expose generic readiness checks and safe branded error pages
d8f2ffd75576210db29be41968a50ca7f6ea4f63 test: define shared authentication throttle and expiry boundaries
65dda8385948de55cf3c6ba0d4142d641ba26ecf security: persist login abuse limits and prune expired throttle records
a3cf413e8f8e45a7a6b4f7608c379144519c086f docs: embed authentic design evidence and actual PostgreSQL release audit
6ec7296f1cea05f06ffce4b7dde7dca38fb3bd6d test: capture brand link accessible-name regression
716f73feb1e9b93de07a99667cef4b1b06f31713 fix: let brand link use its visible accessible text
e6abe6ed52de5608163a63b0cd919665889b8f64 ci: exercise actual Gunicorn workers on the PostgreSQL Linux runner
364ca2fe5965a18d89a603e230237fbad3c6273c security: include current tracked files in the credential-pattern audit
2c41a9f504cd9dc486dfabbe3cfbd6fa964f737a test: capture misleading cancellation action after workshop start
c31e504c7d42b5ee1458bb1919a42a3a4788a163 fix: show cancellation deadline on started workshop bookings
d0241c47271b953b2f91aa3f64f8fb3a79dcf222 docs: record final local release checks and declined Heroku provisioning
```

## Precise continuation and authorisation boundary

1. Paid provisioning is declined. Do not provision a database/dyno/scheduler, deploy a billable process, substitute another provider, or reuse ByteBoard resources without new explicit user authorisation. Preserve the existing empty SkillSeat app record.
2. If the owner later approves exact current costs, reconfirm plans/budget and provision only that app's own Basic/PostgreSQL/Scheduler. Set independently generated Django secrets and explicitly scoped production settings privately; preserve test-only Stripe policy and acquire a dedicated hosted test-webhook signing secret through an authorised flow.
3. Deploy verified synchronized main, verify build/release migrations/static/HTTPS/headers, actual PG version/connection, scoped roles and all hosted user journeys; verify private bytes and database rows survive a real SkillSeat dyno restart. Run and observe scheduled no-traffic expiry, inspect logs, test-only payment verification/replay/late states, resources and eligible reviews. Record actual results.
4. Obtain the actual applicable learner brief/rubric/submission source and reconcile each real criterion with the existing matrix. Do not invent identifiers or substitute student READMEs for institutional criteria.
5. Inspect final-code CI to completion, fix real failures, rerun affected/full checks as warranted, update evidence, push and confirm clean synchronized main. Hosted and institutional evidence gaps prevent Phase4 completion/submission readiness.

The two local fictional release fixture users have been disabled with unusable passwords, their owner permission removed and workshop unpublished; the original Phase3 sandbox financial audit remains untouched. The task-created local Django server and disposable PostgreSQL cluster were stopped gracefully; data is preserved under ignored `.local-tools` for reproducibility. No unrelated service was stopped.
