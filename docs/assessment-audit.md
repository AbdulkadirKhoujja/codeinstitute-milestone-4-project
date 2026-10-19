# Assessment and release requirements-to-evidence matrix

Audit date: 19 October 2026. **The learner-specific authoritative Code Institute MS4 rubric and submission instructions are not yet available.** A request for their accessible source is pending. This is a best-effort audit against the user's supplied Phase 4 requirements and committed README stories, not a claimed institutional rubric or grade prediction.

The public [Code Institute L5 course page](https://codeinstitute.net/global/web-development-level-5/) confirms a four-project course including Django, APIs, authentication, persistence, automated testing and e-commerce. It is contextual evidence only; student repositories and marketing descriptions do not establish exact grading criteria.

| Identified supplied requirement | Implementation / evidence | State | Remaining work / remediation |
| --- | --- | --- | --- |
| Purpose, audiences and user value | README introduction, audience and committed stories | Pass | Retained scope, no unrelated product features |
| Django full-stack CRUD and relational model | Accounts, workshops, bookings, resources and reviews; views/forms/models tests | Pass | Owner scope and server-assigned ownership enforced |
| Authentication and role boundaries | Original account tests, owner/resource/review negatives; new shared throttle tests | Pass | HMAC-keyed DB throttle added; actual hosted verification pending |
| Capacity/booking/payment integrity | Transactional services, constraints and seven races on actual PostgreSQL 17.11 | Pass | Local production-engine verification; hosted PG still pending |
| Stripe test-only fulfillment | Phase 3 actual sandbox exercise plus deterministic payment/signature/replay suite | Pass | Hosted endpoint/sandbox configuration not yet verified |
| Separate Heroku app in ByteBoard account | Account/ByteBoard ownership verified; separate empty app inventory recorded | Partial | User declined Basic/PostgreSQL costs; no dynos/add-ons provisioned, hosted release blocked |
| Production-compatible private storage | Database-backed storage; byte persistence verified across real local PostgreSQL restart | Partial | Implemented/tested locally; Heroku restart/access exercise pending |
| Scheduled expiry without traffic | Existing command releases holds after actual local PG restart, no HTTP requests | Partial | Heroku scheduler installation, schedule and real execution pending |
| Heroku runtime/static/proxy/HTTPS | Procfile, pinned Python, PostgreSQL selection, TLS policy, WhiteNoise, explicit CSRF/proxy settings, health endpoint | Partial | Hosted build, release and HTTPS verification pending |
| Production database integrity/concurrency | 127-test full suite passed against real local PostgreSQL; seven real independent-connection races included | Pass | Record CI and hosted engine/version separately; do not equate local PG with Heroku |
| Dependency vulnerability review | pip-audit 2.10.1 runtime lock audit: no known vulnerabilities | Pass | Point-in-time advisory check, not a guarantee against unknown vulnerabilities |
| Reachable history credential review | scripts/audit_release.py, sanitised JSON; no unresolved pattern findings | Pass | Heuristic plus exact inherited-value checks; documented synthetic unit-test DSN classified, no history rewritten |
| README inline planning/final evidence | Original text wireframes rendered as explicitly dated Phase 4 SVGs; actual screenshots inline | Pass | GitHub inspected: all 11 initial images load, all three Mermaid diagrams render; expanded release captures embedded |
| Original planning provenance | Unchanged 17 October planning source, Phase 4 rendering script | Pass | No original mobile image wireframes existed; explicitly state this |
| Formal HTML/CSS validation | W3C Nu: four local pages, no messages; CSS valid with zero errors/one warning | Pass | POST refusal recorded; documented GET succeeded; hosted validation remains pending |
| Automated/manual accessibility | Phase 3 DOM/keyboard/contrast; actual local Lighthouse standard categories all 100; brand issue fixed test-first | Partial | Hosted and assistive-technology coverage unavailable; no full WCAG claim |
| Responsive/browser journeys | Phase 3 authentic mobile/tablet/desktop captures and flows | Partial | Expand release captures and hosted journeys after access |
| Code quality and regression suite | Ruff, checks and retained 110 Phase 3 cases plus focused release tests | Pass | Continue full SQLite/PG verification after changes |
| Genuine incremental Git development | Separate Red/Green release, storage, retry, health and abuse-control commits | Pass | Final full SHA chronology will be recorded |
| CI completion | Windows preserved; separate PostgreSQL job dispatched | Not Verified | Queued jobs are not passing evidence; inspect actual results |
| Credits/licensing | README credits and implementation choices | Partial | Official source/tool credits reviewed; no repository-wide licence granted. Owner retains licensing decision |
| Final submission instructions/grade thresholds | Authoritative learner-specific source unavailable | Not Verified | User must provide exact applicable brief/rubric/submission source |
| Hosted release and submission readiness | Empty separate app record only; no deployed application, dynos or add-ons | Not Verified | Do not declare Phase 4 complete or submission-ready |

States refer to the specifically described evidence scope. A local Pass never claims an unexecuted hosted test. This matrix must be reconciled with the actual supplied institutional rubric once available, without inventing criterion identifiers.
