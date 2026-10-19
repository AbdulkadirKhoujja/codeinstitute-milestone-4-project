# Assessment requirements → implementation → tests → evidence

19 October 2026. **Phase 4 remains incomplete / not submission-ready.** These are evidence-audit statuses, not an institutional award or predicted grade.

## Actual supplied sources

The learner supplied `asset-v1_CodeInstitute_DIWAD_MS1_2022_Q1_type_asset_block_QS-Diploma-in-Web-Application-Development-Full_Stack_Frameworks.pdf`: Qualification Specification, L5 Diploma in Web Application Development, **Unit 4: Full Stack Frameworks with Django**, unit **F/650/3528**, printed **pp. 55–65 of 66** (11 PDF pages). SHA-256: `bb3d22c11c72a0616cecb417b5e2d886541707fceb791abbc41e3e5e3840bc14`. All eleven pages were extracted; the table containing criterion 3.2 was rendered and inspected. The original PDF remains outside the public repository. [Source provenance](testing/phase4-assessment-source.json).

The learner also supplied **13 mandatory requirements**, including original frontend JavaScript (8) and Stripe test payments unlocking content (6). Those exact supplied numbers are mapped separately below. The previous marketing-page context is superseded; no criterion identifiers are invented. Separate submission administration or an assessor's final judgement is not inferred.

**PASS**: supporting evidence for the described scope. **PARTIAL**: implemented/evidenced in part, with stated gaps. **FAIL**: observed unmet requirement. **NOT VERIFIED**: required execution/evidence absent. A scoped PASS never implies perfect security, universal accessibility or an awarded grade.

Runtime snapshot: `e06fce0a855a650afd75469ffcd089a1469813b2`, Heroku **v19**, PostgreSQL **18.4**. [Hosted journeys](testing/phase4-live-journeys.json), [CI](testing/phase4-live-ci.json), [local/TDD checks](testing/phase4-live-checks.json), [deployment](testing/phase4-live-deployment.json), [screenshots](testing/phase4-production-screenshots.json). The final documentation publication has its own SHA/release and CI result in the delivery record.

## Thirteen supplied mandatory requirements

| Requirement | Implementation | Test | Evidence | Status / gap |
| --- | --- | --- | --- | --- |
| 1. Django full stack / relational data | Django views/templates and PostgreSQL domain records | Full suites, DB checks, genuine restart | CI; live baseline/journeys | PASS |
| 2. New multi-app project | `core`, `accounts`, `workshops` | Foundation wiring tests | Source, architecture, phased history | PASS |
| 3. Domain schema / at least two custom models | Workshop, Booking, Resource, Review, payment models and custom user | Model/constraint/race tests | README ERD, migrations, PostgreSQL CI | PASS |
| 4. Reasoned user registration/login | Identity scopes bookings, profile, reviews and resources | Account tests; hosted registration/login/logout/profile | Live journeys and account screenshots | PASS |
| 5. Validated non-authentication create/edit forms | Owner workshop and attendee review forms | Invalid/valid hosted submissions; ownership and form tests | Live journeys; editor captures | PASS |
| 6. Stripe test commerce unlocking content | Checkout, signed fulfillment, paid+confirmed access | Payment/signature/resource suite; genuine Phase 3 sandbox | Historical provider evidence; current safe-disabled feedback | **PARTIAL** — Heroku test key/signing secret absent; current successful payment and paid content unlock NOT VERIFIED |
| 7. Navigation / structured layout | Shared semantic navigation and responsive wrapping | Interface/keyboard/viewport checks | Inline production screenshots; responsive JSON | PASS in tested scope |
| 8. Custom frontend JavaScript | Progressive booking-cancellation confirmation | Three Node behavior cases, syntax/JSHint, template integration | Red `36625a3` → Green `e06fce0`; CI; browser cancellation | PASS — browser dismissal limitation explicitly recorded |
| 9. README purpose / user value | Audience, stories, features, diagrams, design, setup and results inline | Target checks and GitHub render inspection | Main README | PASS in documented scope |
| 10. Git and GitHub | Genuine small Red/Green/feature/fix commits | History review, remote comparison, CI | Git history and release chronology | PASS |
| 11. Separation / attribution | Original source separate from locked dependencies; credits | Source/README review | Credits and requirements files | PASS within reviewed source |
| 12. Final hosted application | Existing Heroku build/release, Gunicorn, PostgreSQL, WhiteNoise | Slug SHA, health, migrations and hosted journeys | Deployment JSON; final delivery record | PASS for deployment; payment gap remains under 6 |
| 13. No secrets / DEBUG off | Environment policy, ignored local secrets, hashed passwords | Environment/release/security tests; deploy/source checks | Live baseline and scoped source audit | PASS within documented checks |

## Unit 4 pass criteria

Page references are the printed PDF pages, not invented rubric IDs.

| Criterion (page) | Implementation | Test | Evidence | Status / limitation |
| --- | --- | --- | --- | --- |
| 1.1 Django/relational/multi-app design (55) | Original planning, ERD and app boundaries | Foundation/model tests | README wireframes/architecture | PASS |
| 1.2 Accessible purposeful interactive UX (55) | Labels, landmarks, skip/focus/status/error states, responsive layouts | Interface, keyboard/DOM and Lighthouse checks | Production captures and validation JSON | PARTIAL — scoped Chromium evidence; full WCAG/physical-device/screen-reader coverage not claimed |
| 1.3 Implement interactive Django multi-app relational site (55–56) | Accounts, studio, bookings, reviews/resources | 132 Django tests per backend; hosted journeys | Runtime CI/live evidence | PASS; specific commerce gap under 4.1 |
| 1.4 Validated model create/edit form (56) | WorkshopForm, ProfileForm, ReviewForm | Hosted valid/invalid requests and form tests | Live journeys | PASS |
| 1.5 Logical Django file structure (56) | Standard project/app URLs, models/forms/views/services/templates/static | Wiring/import/runtime tests | Source; architecture | PASS |
| 1.6 Clean code (56) | Named services and separate payment/storage policies; project Ruff style | Ruff lint/format, JSHint, source review | CI; live checks | PASS within reviewed style/source scope |
| 1.7 Consistent URLs (56) | Namespaced routes and reverse resolution | URL/view/template tests; hosted routes | README route table | PASS |
| 1.8 Navigation and structured layout (56) | Shared navigation and landmarks | Interface/three-size browser checks | Responsive JSON/captures | PASS |
| 1.9 Custom Python logic (56) | Reservations, transaction retries, event matching, access rules | Booking/concurrency/payment/resource tests | Source; hosted final-seat race | PASS |
| 1.10 Compound statements in functions (56) | Conditional/loop services, payment and permission logic | Positive/negative branch tests | Services/payments/views and tests | PASS |
| 1.11 Planned functionality/usability/responsiveness/data tests (56–57) | Automated suites plus controlled hosted plan | Full CI, HTTP races, keyboard/viewport tests | README testing/live evidence | PARTIAL — current hosted provider success/failure/replay cases absent |
| 2.1 Clear relational schema (57) | FKs, uniqueness/check constraints, historical booking states | Constraint/migration tests | Inline ERD/constraint table | PASS |
| 2.2 At least two original custom models (57) | Workshop, Booking, Resource, Review and payment entities | Domain tests | Models/migrations/README | PASS |
| 2.3 Validated non-authentication create form (57) | WorkshopForm and ReviewForm | Hosted invalid and valid submissions | Live journeys | PASS |
| 2.4 All CRUD operations (57) | Workshop create/read/edit; review create/read/edit/delete; resource upload/read/delete | Hosted CRUD and private-byte deletion; automated owner negatives | Live journeys; ownership/resource tests | PASS — workshops retain booking history intentionally; review/resource deletion demonstrates DELETE |
| 3.1 Reasoned authentication (57) | Personal bookings/resources/reviews require identity | Real register/login/logout/profile; account suite | README purpose; live evidence | PASS |
| 3.2 Login/register only for anonymous users (57) | LoginView redirect and registration guard before save | Red regression tests; hosted GET redirects and POST no-create | `2157fad` → `ca81b89`; live journeys | PASS — discovered from supplied rubric and corrected |
| 3.3 Non-admin direct datastore access prevented (57) | No published DB credentials/admin client; server ORM and permissions | Owner/resource/admin negatives; config checks | Security tests/live policy | PASS within app access scope; no exhaustive provider-network penetration test |
| 4.1 Hosted e-commerce processing (57–58) | Test-only Checkout, signatures, idempotent receipts | Deterministic suite and earlier genuine sandbox | Phase 3 evidence; current disabled checkout | **PARTIAL** — current Heroku key/signing secret absent |
| 4.2 Successful/unsuccessful purchase feedback (58) | Server payment states and API-error feedback | Payment/interface tests; hosted missing-config feedback | Booking captures; Phase 3 provider record | **PARTIAL** — current hosted success/provider-failure feedback needs actual sandbox execution |
| 5.1 Final deployment / development parity (58) | Same source/locks deployed on Heroku | Slug SHA, health, migrations and core journeys | v19 snapshot; final publication delivery | PASS in tested source/parity scope |
| 5.2 No commented-out code / broken internal links (58) | Active runtime source reviewed; namespaced links and safe recovery | Interface/route tests; hosted public-link checks | Source and live HTTP/browser evidence | PASS within reviewed source/exercised routes |
| 5.3 Deployed security / hidden secrets / DEBUG off (58) | Explicit production policy, HTTPS/CSRF/cookies/HSTS/throttle | Deploy check, negative requests, scoped source scan | Baseline/operations/journeys | PASS within described checks |
| 5.4 Regular Git commits and README (58) | Genuine Red/Green fixes and release documentation | Actual history review | Chronology/README/GitHub | PASS |
| 5.5 Consistent Markdown README (59) | Substantial inline screenshots/diagrams and structured prose | Target/render checks | README/render evidence | PASS |
| 5.6 Deployment/database/testing/purpose/value documented (59) | Full manual release/config/database/testing instructions | Procedure checked against actual baseline/builds | README and release report | PASS — outstanding Stripe/schedule steps clearly labelled |

## Merit and distinction evidence

| Criterion | Implementation → test → evidence | Status |
| --- | --- | --- |
| M(i) Purposeful intuitive UX, user control, immediate CRUD feedback | Clear hero/audience, scoped navigation and real CRUD messages; browser/interface tests; inline screenshots | PARTIAL — commerce disabled and broader accessibility/dialog limits documented |
| M(ii) Robust codebase | Constraints, PG17/18 races, defensive input/API handling; full suites and hosted negatives; CI/live evidence | PARTIAL — current hosted provider verification incomplete |
| M(iii) TDD demonstrated in commits | Separate failing-test and Green commits throughout earlier phases and three continuation slices; actual hashes/outcomes in release/live checks | PASS |
| M(iv) Efficient Procfile/requirements/settings/database config | Hash locks, explicit config selection, actual Gunicorn smoke/build/release | PASS in tested configuration |
| M(v) Schema fully described in README | Inline ERD, entities, FKs, constraints, blob key, state/workflow diagrams | PASS |
| M(vi) Appropriate template/model/business logic placement | Templates present data; models constrain it; services/payments handle transactions; views orchestrate requests; tests and README architecture | PASS within reviewed architecture |
| M(vii) Effective version-control record | Genuine chronological commits, no rewritten history/artificial splits, CI per pushed revision | PASS within inspected history |

The qualitative distinction characteristics/craftsmanship amplification (pp. 60–65) are not assigned invented numbered criteria. Planning provenance, purposeful content, schema, CRUD, security, validation and genuine TDD evidence exist. Fully functioning hosted commerce and broader browser/accessibility/provider-operation evidence remain gaps. No distinction or other grade is asserted.

## Additional supplied Phase 4 release requirements

| Requirement | Implementation → test → evidence | Status / next step |
| --- | --- | --- |
| PostgreSQL 18/concurrency | Actual production18.4, CI17/18 full132 each, hosted two-request final-seat race | PASS |
| Restart/private-byte persistence | Exact fictional handout and blob SHA survived genuine restart of existing web dyno | PASS |
| Pending-hold expiration | Fixture timestamp deliberately moved into past; actual hosted discovery expired it and restored capacity | PASS for request-triggered execution |
| Scheduled expiry without traffic | Idempotent maintenance command exists; no scheduler attached | NOT VERIFIED — no extra service/dyno provisioned under resource restriction |
| Current hosted Stripe signed success/replay/late/expired cases | Strong tests and earlier real provider exercise; no current Heroku credentials | NOT VERIFIED — configure privately, then execute real sandbox flow; never synthesize a PASS |
| Paid-attendee private download | Owner exact-byte access and unpaid denial hosted; paid policy tested automatically | PARTIAL — actual current hosted payment needed |
| Responsive/keyboard/validation | Three emulated sizes; twelve sampled combinations; skip/focus; four-page W3C; CSS0 errors/1 warning; hosted Lighthouse100s | PASS for scoped checks; full accessibility remains PARTIAL |
| Authentic inline screenshots | 22 real hosted captures plus original text wireframes and separately labelled local history | PASS with manifest provenance |
| Safe cleanup | Exact fictional rows/private bytes and fixture sessions removed; initial domain-record counts restored; throttle counters preserved | PASS |
| CI/final publication | Runtime all three jobs green; documentation-only final revision separately checked/deployed before delivery | Final exact SHA/release/CI result recorded in delivery; no queued run counted as success |

**Readiness:** do not describe the submission as fully verified while mandatory requirement 6 / criteria 4.1–4.2 remain partial. Finish the actual hosted Stripe test payment/content-unlock path and the requested scheduled no-traffic expiry under an authorised arrangement. Address remaining browser/accessibility limits proportionately; Lighthouse is not full WCAG certification.
