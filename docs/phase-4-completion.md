# Phase 4 completion and submission-readiness decision

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
