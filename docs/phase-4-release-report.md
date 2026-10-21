# Phase 4 release and submission-readiness report


21 October 2026. **Phase 4 is complete within the supplied project scope and ready for assessment submission.** This is an evidence-based readiness decision, not an institutional award or predicted grade.

## Verified outcomes

| Scope | Actual evidence |
| --- | --- |
| Genuine hosted Stripe commerce | v22 £1 sandbox decline/success, direct signed fulfillment, two provider resends, one receipt/seat, confirmation and exact purchased download; evidence published in `03e7821`, all three CI jobs passed |
| Unattended hold expiry | Heroku v23, source `8aeb4e2d5ef142171f8d9abfc2e1dfcd517fa8f5`; observed no-traffic timer release and recovery after restarting the existing web dyno. |
| No website visits | Router requests during observed window: **0**, from 2026-10-21T18:10:23.098078+00:00 to 2026-10-21T18:12:31.139285+00:00 |
| Expiry timing | First hold observed released 21.021s after due; after restart 37.037s after due; five-second DB sampling, not exact execution latency |
| Preservation | Future hold stayed pending; pre-existing users/workshop/bookings/payment attempts/event receipts unchanged; payment-free fixtures removed |
| Resources | Same one Basic web dyno and own Essential-0 PostgreSQL attachment; no scheduler add-on, extra dyno or new billable resource |
| TDD | `ddc9afc`: five genuine failures; `8aeb4e2`: five pass; complete local 137 tests passed in 29.035s; lint/format/migrations/whitespace pass |
| CI | [Scheduler run 39649848477](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39649848477): 137 tests on Windows, PostgreSQL 17 and 18; seven separate SQLite races; actual Gunicorn hooks/smoke pass |

## Arrangement and limits

`Procfile` loads `config/gunicorn.py`. After Django initializes in each forked worker, a daemon thread immediately invokes the existing management command, then waits 60 seconds after completion before its next attempt. Failures log a generic error and retry next tick. Connections close after each attempt. Worker exit signals/stops the thread; replacement workers resume it and catch up overdue holds. Existing transaction/idempotency and concurrency tests protect duplicate workers/ticks. The command also prunes expired authentication counters as before.

This uses the already-running Basic web dyno. It depends on web-worker availability; outage/scaling to zero delays cleanup until restart. Request-driven expiry remains a fallback and booking/payment rules still enforce hold deadlines. A dedicated independent scheduler/worker and alerts would improve operational separation but are optional, potentially billable infrastructure. [Heroku documents that Scheduler jobs consume one-off dyno usage](https://devcenter.heroku.com/articles/scheduler#dyno-hour-costs). No additional billable resource was provisioned.

## Mandatory assessment versus enhancements

All 13 supplied mandatory requirements have supporting scoped PASS evidence, including actual Stripe test-mode content unlock. The Unit 4 pass-criteria matrix maps all 26 criteria; guideline/UX checks and planned manual/automated testing are assessed in their executed scope, without treating absent universal certification or every possible device/payment-method test as an observed mandatory failure. The broader merit/qualitative caveats remain visible. [Assessment audit](assessment-audit.md).

Unattended expiration was an additional user-requested release requirement, beyond the supplied 13 mandatory project requirements, and is now complete. Broader physical-device/Firefox/Safari/screen-reader checks, hosted late/asynchronous payment methods, independent scheduling/alerts and formal certification remain optional improvements. No live payment or credential disclosure occurred. No grade is guaranteed, and separate institutional submission administration is not inferred.

## Publication and evidence

- [Actual unattended execution, sanitized logs and cleanup](testing/phase4-unattended-expiry.json)
- [Production security, migrations, links and secret scan](testing/phase4-completion-checks.json)
- [Genuine TDD and local results](testing/phase4-scheduler-tdd.json)
- [Exact completed Stripe/scheduler CI runs](testing/phase4-completion-ci.json)
- [Preserved v22 payment evidence](phase-4-hosted-stripe.md)

The final documentation-only commit is pushed, deployed and checked after this report is saved. Its exact SHA/release and completed CI result are reported in final delivery and provider history, avoiding a self-referential hash. Verification snapshots above retain their real source/release identity.

## Historical payment and release checkpoints

The snapshots below preserve earlier limitations; their open/incomplete decisions are superseded by the actual completion evidence above.


## Current commerce update — 21 October 2026

**The mandatory hosted commerce gap is resolved in the executed sandbox card scope.** Heroku **v22**, source `3d28b6858c72132b1d86a93aba8822aaa429c595`, completed a genuine £1 test Checkout, user-submitted decline/success, direct signed fulfillment, two Stripe resends with one durable receipt/seat, confirmation and exact HTTP/browser protected download. A separate genuine provider expiry released its hold. Invalid signatures and modified bytes returned400. Twenty payment/resource tests and production deploy checks passed. [Detailed report](phase-4-hosted-stripe.md), [sanitised results](testing/phase4-hosted-stripe.json).

The user explicitly approved creating the missing sandbox endpoint and privately configuring its signing secret. Existing live Stripe settings and unrelated endpoints were untouched. Fixture accounts were disabled, workshop unpublished, sessions/handout/private bytes removed; sandbox financial audit records were retained with reconciled capacity. **Phase 4 remains open for scheduled no-traffic expiry evidence** and the stated broader testing limits. The following 19 October report is a historical snapshot; its missing-Stripe statements are superseded by this update.


19 October 2026. **Deployment successful; Phase 4 incomplete / not submission-ready.** The current Heroku deployment has no Stripe test key or hosted webhook signing secret, so mandatory commerce/content-unlock verification is still missing. No fifth phase was created.

## Independently established production baseline

Local and remote `main` both started at `b546e4976110839f06178264492bf91eb5f9316d`, clean. Heroku **v16** had successfully deployed that exact slug commit, with one existing Basic web dyno and one existing Essential-0 PostgreSQL attachment. Actual server version was **18.4**, all migrations were applied, `check --deploy --fail-level WARNING` passed, and the application's user/workshop/booking/private-blob counts were zero. The old declined-provisioning report was therefore stale. [Sanitised actual baseline](testing/phase4-live-baseline.json).

This continuation reused the existing SkillSeat app, attachment and manual build/release arrangement. It did not provision an add-on, scheduler, subscription or extra dyno, reset a database, or modify ByteBoard. The only restart was of the existing SkillSeat web process for the required persistence test. Historical source/evidence and genuine Phase 3 sandbox financial records in the local development database were retained.

## Verified runtime and exact evidence scope

| Item | Actual observed result |
| --- | --- |
| Public URL | https://skillseat-akkhoujja-e88f42c60993.herokuapp.com/ |
| Heroku app | `skillseat-akkhoujja`, EU, heroku-24/Cedar |
| Runtime verification SHA | `e06fce0a855a650afd75469ffcd089a1469813b2` |
| Runtime verification release | **v19**, succeeded, 19 October 2026 21:01:31 UTC |
| Previous continuation deployments | v17 discovery filters (`8cf5220`); v18 anonymous-only auth (`ca81b89`), both succeeded |
| Production database | Existing own Essential-0 attachment; actual PostgreSQL **18.4**; no unapplied migrations |
| Production security | DEBUG false, explicit host/origin, Heroku proxy policy, secure cookies, HSTS/HTTPS, CSRF/owner/resource denials, shared throttle verified |
| Static and logs | Hashed CSS/JS/favicon HTTP 200; immutable CSS caching; inspected app log window contains no traceback or Heroku H error code; expected negative-test403/404/503 are documented |
| Current hosted functional checks | **35 PASS** observations in the current recorded HTTP/DB journey set; see exact items and fixture caveats below |
| Genuine restart persistence | Existing web dyno restarted; exact fictional private bytes/blob SHA and authenticated owner download survived |
| Cleanup | Exact fixture users/workshops/bookings/reviews/private bytes/sessions removed; domain-record counts match zero baseline; auth counters retained |
| Full local Django suite | **132 passed in 25.619s**, using a writable workspace TEMP |
| Windows CI | **132 passed in 6.023s**, plus seven file-backed races in 0.323s |
| PostgreSQL 17 CI | **132 passed in 6.830s**, including seven independent-connection races; actual Linux Gunicorn smoke passed |
| PostgreSQL 18 CI | **132 passed in 8.966s**, including seven independent-connection races; actual Linux Gunicorn smoke passed |
| Frontend JavaScript | Three Node behavior tests, Node syntax and JSHint 2.13.6 pass; served as hashed static source |
| Other checks | Ruff lint/format, uv dependency consistency (17 packages), system/deploy checks, migration consistency and whitespace pass |
| Runtime CI | [39324116798](https://github.com/AbdulkadirKhoujja/codeinstitute-milestone-4-project/actions/runs/39324116798): Windows + PG17 + PG18 all success |
| Earlier queued CI | Runs 39284481374 and39285069472 are now success; 39322577679 filters and39323852089 auth correction also success |
| Hosted W3C HTML | Actual home/discovery/register/login HTML: no messages; transient CSRF tokens removed before submission |
| W3C CSS | Valid, zero errors, one system-font vendor-extension warning |
| Hosted Lighthouse 13.5.0 | Mobile actual public home: **100 performance/accessibility/best practices/SEO**, no failing accessibility audits; FCP/LCP0.9s, CLS0, TBT0ms |
| Responsive and keyboard | Twelve hosted page/size combinations at390×844,768×1024,1440×1000 without horizontal overflow, unlabelled controls or unnamed buttons; skip link focuses main; visible focus checked |
| Production images | **22 genuine captures**, inline README; fictional/sanitised records only; JPEG headers/dimensions/hash manifest checked. Actual GitHub inspection at8cdfb74: all38 inline images loaded and all three Mermaid diagrams rendered |
| Assessment sources | Supplied actual Unit 4 specification F/650/3528, pp55–65; all 26 pass criteria and7 merit criteria mapped, plus all 13 mandatory requirements |

The tables identify a **verification snapshot** rather than attempting to embed a Git commit's own hash within itself. The final documentation-only publication retains this runtime code; its exact final SHA, Heroku release and completed CI URL are recorded in the delivery response and actual provider histories. It must be deployed and checked before delivery; a queued run is not treated as success.

## Actual hosted journeys and limitations

The current v19 run exercised registration of three fictional users, secure-cookie login, own profile editing, logout, anonymous-only login/registration GET redirects and authenticated registration POST rejection, attendee studio denial, missing-CSRF rejection, invalid form feedback, owner draft creation/edit/publication, non-owner edit denial and combined text/price filtering.

Two independently authenticated public requests competed for a one-seat free workshop. Exactly one confirmed booking and one reserved place resulted. Another user's cancellation was denied; own cancellation released capacity. A paid fixture created a pending hold, Checkout clearly reported missing configuration and no paid flag was granted. The unconfigured webhook rejected input with 503. Moving only the fictional hold's expiry timestamp into the past and issuing a real discovery request expired it and restored capacity. This proves request-triggered cleanup, **not** unattended scheduled execution.

An owner uploaded/downloaded the exact fictional handout; anonymous access redirected to login and unpaid access returned 404. A simulated event was deliberately backdated, attendance recorded through hosted owner POST, and the attendee created then edited/deleted a review through hosted forms. Resource deletion through its owner form also removed database bytes. No real attendance or payment was claimed. Temporary future dates used for representative screenshot layouts were restored/backdated only on these controlled fixtures.

Native browser cancellation completed and a real screenshot records its success. The in-app browser's CDP timed out while operating `window.confirm`; hosted dismissal is **NOT VERIFIED**. The three isolated JavaScript behavior cases verify acceptance/dismissal and ordinary/prevented forms. A repeated throttle probe initially reused an already-throttled name, invalidating its fresh-bucket expectation; a fresh nonexistent alias verified five failed attempts followed by 429 with Retry-After/no-store without resetting production counters. These tooling observations are retained, not disguised as product fixes.

Current successful Stripe Checkout, signed fulfillment, confirmation, rejected/replayed/late/expired provider events and paid-attendee resource download are **NOT VERIFIED on Heroku**. Both `STRIPE_TEST_KEY` and `STRIPE_WEBHOOK_SECRET` are absent. Earlier genuine Phase 3 sandbox payment/signature/replay evidence and deterministic tests remain valid in their own scope; they are not relabelled as current hosted passes. No live payment was initiated.

No scheduler is attached, and the user prohibited provisioning more services/dynos. Scheduled no-traffic expiration remains **NOT VERIFIED**. Physical devices, Firefox/Safari, screen readers and full WCAG compliance are also not claimed. The hosted site honestly shows an empty workshop state following fixture cleanup.

## Genuine corrections, with Red → Green evidence

1. Missing discovery filtering: two newly failing tests preceded case-insensitive title/description/location search and free/paid filters. Five discovery tests passed; 129-test suite passed; CI gained PostgreSQL 18 coverage alongside17.
2. Supplied Unit 4 criterion3.2: two regression tests produced three failing subcases for authenticated access/account creation. The LoginView redirect and early registration guard fixed them; 131 tests passed and real hosted GET/POST checks passed.
3. Supplied mandatory requirement8: three JavaScript behavior tests failed because the custom script was absent, and the template integration test failed. Progressive cancellation confirmation and its external deferred script then passed; final132 Django +3 JavaScript tests passed. JSHint's global-strict finding was corrected with a function wrapper, without suppressing the rule. Existing server-side CSRF/permission checks were preserved.

The first local test attempt lacked an explicit strong development key; a later sandbox TEMP restriction caused filesystem-test errors. Rerunning with an ephemeral private key and writable workspace TEMP produced the actual passing results. The uv environment has no pip; dependency consistency was checked correctly with `uv pip check`. No failed execution is described as a pass.

## README, visuals and assessment audit

The current ByteBoard README was fetched read-only as a presentation reference. SkillSeat's main README now prominently links the live application and includes substantial purpose/stories/features, original planning provenance, wireframes, inline production desktop/mobile/tablet/account/owner/booking/resource/error/empty screenshots, ERD/architecture/state diagrams, role/payment rules, actual validation/results and full existing-app deployment/database instructions. The22 production captures are separate from preserved historical local captures. The supplied source PDF was hashed and inspected, not republished in the public repository.

[Assessment matrix](assessment-audit.md): all 26 actual pass criteria,7 merit criteria and13 supplied mandatory requirements trace implementation → tests → evidence → status. **Mandatory6 / Unit 4 4.1–4.2 remain PARTIAL** because hosted commerce/content unlock is unverified. Broader accessibility/testing characteristics remain PARTIAL in their stated scope. The rubric is now available; the prior claim that it was unavailable is superseded. No grade prediction is made.

## Completion decision and remaining work

**Do not mark Phase 4 complete or claim full submission readiness.** Deployment, core CRUD/auth/booking, production PostgreSQL 18 compatibility, restart persistence, documentation and available CI are verified. Remaining essential work is to configure existing Stripe sandbox credentials and the real hosted signing secret privately, then execute the actual hosted payment/provider-event/paid-resource journey. Do not paste credentials into chat, source or evidence. Verify scheduled no-traffic expiration only under an authorised arrangement; do not provision an extra resource as a workaround. Record native-dialog/browser/assistive-technology limits proportionately.

The former provisioning refusal is preserved as historical context only: the previous checkpoint had an empty app. By this continuation's baseline, the owner had successfully deployed v16 with its own database/web process. No further resource was bought, no other project changed and no database reset occurred.

## Genuine Phase 4 commit history

Original release-engineering commits retained unchanged:

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

The continuation began from `b546e4976110839f06178264492bf91eb5f9316d`. Six implementation/TDD commits through the verified runtime:

```text
bf99ae4d0c40e3e465cd601dcbf1fe700c4a6e68 test: capture missing discovery search and price filters
8cf522097601f7baac7b8465c7e3390f611a810f feat: add accessible workshop discovery filters and verify PostgreSQL 18
2157fad3a919188a7b798a59901ff606840ef1dc test: enforce anonymous-only authentication pages from Unit 4 criterion 3.2
ca81b890ac08d3dfa1013178414945f8db2eacdb fix: restrict login and registration forms to anonymous users
36625a395b128894b164332b01230a8f8b21e1f3 test: specify cancellation confirmation as a frontend enhancement
e06fce0a855a650afd75469ffcd089a1469813b2 feat: confirm booking cancellation with tested custom JavaScript
```

The final evidence/documentation publication commits are identified in delivery after review, push, rendered-README verification and deployment. No manufactured commits or history rewriting were used.

## Evidence index

- `testing/phase4-live-baseline.json`: initial actual v16 release, policy, PG18.4/migrations and zero-record baseline.
- `testing/phase4-live-deployment.json`: v19 runtime build/release result and full source SHA.
- `testing/phase4-live-journeys.json`: exact current hosted positives/negatives, simulated-fixture caveats and browser/tool observations.
- `testing/phase4-live-operations.json`, `phase4-live-links.json`: sanitised logs, readiness and actual public anchors/static assets.
- `testing/phase4-live-cleanup.json`: scoped deletion and restored baseline counts.
- `testing/phase4-live-ci.json`, `phase4-live-checks.json`, `phase4-live-sqlite-tests.txt`: runtime jobs, TDD and actual local output.
- `testing/phase4-live-*-validation.json`, `phase4-live-lighthouse.json`, `phase4-live-responsive.json`: actual hosted audits, separated from historical local files.
- `testing/phase4-production-screenshots.json`: capture origin/provenance, file format/dimensions and hashes.
- `testing/phase4-assessment-source.json`: supplied institutional source fingerprint and scope.
