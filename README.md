# SkillSeat

SkillSeat is the working title for a Code Institute Milestone Project 4 full-stack Django application.

## Project overview

This repository is currently at the planning and repository-foundation stage. SkillSeat is not yet implemented, so this README records the committed product direction without presenting planned work as completed functionality.

## Purpose and intended audience

SkillSeat is planned as a full-stack Django workshop and training discovery and booking platform. It is intended to help people discover relevant workshops, register and manage participation, and access resources associated with paid attendance.

The intended audiences are:

- public visitors discovering workshops;
- registered attendees booking workshops and managing their participation; and
- workshop owners and administrators managing listings and related workflows.

## Current development status

- Phase 1 has started with repository security, product definition, and documentation foundations.
- Django has not been initialised.
- No application features, routes, models, tests, screenshots, or deployment have been implemented.
- The README will be updated alongside the application and verification evidence.

## Planned product scope

The following is the committed core scope. Every item is planned and requires implementation and verification before it can be described as complete:

- public workshop discovery and workshop detail pages;
- registration, login, logout, and account management;
- workshop listing management for authorised owners and administrators;
- booking, cancellation, and server-enforced capacity controls;
- attendee reviews;
- Stripe test-mode payments with a verified payment state; and
- access-controlled workshop resources for paid attendees.

No optional enhancements are committed at this stage. They will only be considered after the core scope, tests, accessibility evidence, and documentation are complete.

## User stories and acceptance criteria

These concise stories define the initial testable scope. They are planning requirements, not evidence of implemented functionality.

### Committed core stories

**P0 — Anonymous visitor discovers a workshop**

As a public visitor, I want to browse workshops and open their details so that I can decide whether a workshop is relevant to me.

Acceptance criteria:

- workshop discovery is available without authentication;
- a workshop detail view presents the information needed to evaluate it; and
- an unavailable or invalid workshop does not expose unrelated records or internal errors.

**P0 — Visitor creates and uses an attendee account**

As a visitor, I want to register, sign in, sign out, and manage my account so that my participation is associated with my own identity.

Acceptance criteria:

- registration validates required input and does not reveal sensitive account information;
- login and logout provide clear success or failure states; and
- account actions cannot be used to access another attendee's account.

**P0 — Attendee books within capacity**

As an authenticated attendee, I want to book an available workshop so that I can reserve a place.

Acceptance criteria:

- only authenticated attendees can create bookings;
- a booking cannot increase attendance beyond the workshop capacity;
- concurrent booking attempts must respect the final available seat without overselling, with automated concurrency verification required during implementation;
- repeated booking attempts do not create duplicate active bookings for the same attendee and workshop; and
- the attendee can see the resulting booking state.

**P0 — Attendee cancels their booking**

As an authenticated attendee, I want to cancel my own booking so that my place can become available to someone else.

Acceptance criteria:

- an attendee can cancel only their own eligible booking;
- cancellation releases the reserved capacity according to the implemented booking rules; and
- an attendee cannot cancel or alter another attendee's booking.

**P0 — Attendee pays with verified test-mode payment**

As an attendee, I want to pay through Stripe test mode so that a paid booking has a trustworthy payment state.

Acceptance criteria:

- payment uses Stripe test credentials and never exposes secret credentials in client-side code or Git history;
- a booking is not treated as paid solely because a client reports success;
- the server records payment as verified only after the agreed Stripe confirmation flow;
- failed, cancelled, or expired payment attempts cannot permanently consume workshop capacity;
- the booking hold, payment expiration, and capacity-release policy is explicitly documented and tested during implementation;
- payment confirmation is verified server-side; and
- repeated provider notifications are handled idempotently and cannot process the same payment twice.

**P1 — Paid attendee accesses workshop resources**

As an attendee with a verified paid booking, I want to access the resources for that workshop so that I can prepare for or continue my training.

Acceptance criteria:

- access is granted only for the relevant workshop and verified paid booking;
- anonymous users, unpaid attendees, and attendees without the relevant booking are denied; and
- owners and administrators can manage resource access without exposing unrelated private resources.

**P1 — Attendee submits a review**

As an eligible attendee, I want to submit a review for a workshop I attended so that I can record useful feedback.

Acceptance criteria:

- a confirmed booking alone does not establish review eligibility before the workshop has taken place;
- review eligibility follows a documented attendance or completion policy and is enforced and tested server-side;
- an eligible authenticated attendee can submit one review for that workshop;
- an attendee can manage only their own review for that workshop; and
- review content is validated and displayed according to the moderation and visibility rules defined during implementation.

**P0 — Workshop owner manages their listings**

As a workshop owner, I want to create and manage my own workshop listings so that the public information remains accurate.

Acceptance criteria:

- an authorised owner can create, edit, publish, unpublish, or otherwise manage only their own listings;
- submitted ownership is assigned or verified server-side; and
- one owner cannot read or modify another owner's protected management data.

**P1 — Owner or administrator manages related workflows**

As an authorised workshop owner or administrator, I want to manage capacity, bookings, and workshop resources within my authority so that the platform remains operational.

Acceptance criteria:

- owners are restricted to workshops they own;
- administrators can perform the explicitly defined administrative actions across the platform;
- capacity changes cannot create an invalid overbooked state; and
- every protected action enforces authorization on the server, not only in the interface.

**P0 — Platform protects role and data boundaries**

As a platform maintainer, I want permission checks and payment state checks to be enforced server-side so that private data and paid resources are not disclosed.

Acceptance criteria:

- anonymous users cannot access authenticated, owner, administrator, or paid-resource actions;
- attendees cannot perform owner or administrator actions;
- owners cannot cross their ownership boundary;
- object-level authorization is covered by tests; and
- invalid identifiers, forged form data, replayed requests, and altered client-side payment states fail safely.

## Development phases

Development will remain within four phases. Implementation will follow strict Red → Green → Refactor TDD, with many small, meaningful commits that keep code, tests, and documentation aligned.

### Phase 1: Repository Foundation

Objective: establish a safe, documented, reviewable project baseline.

Deliverables: repository protections, the product direction, prioritised user stories, four-phase plan, and the documentation roadmap.

Completion criteria: only safe project foundations are committed; no secrets or local artefacts are tracked; the README distinguishes planned scope from implemented evidence; and independent review can verify the baseline.

### Phase 2: Django Foundation

Objective: create the smallest working Django foundation needed for tested development.

Deliverables: project configuration, dependency definitions, environment configuration guidance, initial application structure, initial data model decisions, and the first Red → Green → Refactor test slices.

Completion criteria: the foundation runs locally, configuration is documented, initial security boundaries are tested, and no feature is described as complete without passing evidence.

### Phase 3: Core SkillSeat Features

Objective: implement the committed discovery, account, workshop management, booking, capacity, review, payment, and resource-access scope.

Deliverables: incremental models, views, templates, forms, permissions, payment integration, resources, tests, design evidence, and documentation updates.

Completion criteria: each committed user story has passing relevant tests, including permission, capacity, and payment-state cases; responsive and accessible behaviour has evidence; and documentation matches the implementation.

### Phase 4: Release and Evidence

Objective: prepare, verify, and honestly document a releasable application.

Deliverables: production configuration, deployment evidence, security review, Git-history secret scanning, browser and accessibility checks, final screenshots, known limitations, credits, and reflection.

Completion criteria: release checks are reproducible, deployment claims are supported by recorded evidence, unresolved limitations are explicit, and the final README makes no unsupported claims.

## Documentation roadmap

Documentation will evolve with the real implementation. Planned documentation includes:

- wireframes and design rationale, with planned-versus-final comparisons for major journeys;
- data model entities, relationships, constraints, migrations, and ownership rules;
- routes, permissions, protected resources, and user journeys;
- technology choices, dependency rationale, and version records;
- local setup, environment configuration, and safe test credentials guidance;
- unit, integration, permission, payment, and browser testing evidence;
- responsive design decisions and accessibility evidence across relevant views;
- deployment steps, production configuration, and verification results;
- security review, including Git-history secret scanning and authorization boundaries; and
- known limitations, credits, and an honest reflection on decisions, challenges, and learning.

## Design and wireframes

Design evidence will be prominent and traceable. For each major journey, the README will distinguish the original planning artefact, the implemented result, and the comparison between them. If a wireframe or final capture does not exist, that absence will be stated rather than reconstructed retrospectively. No wireframes or screenshots are available yet.

## Features

No features are currently implemented. The committed scope and user stories above are planned requirements; completed features will be listed here only after implementation and verification.

## Data model

No data model has been designed or implemented yet. Confirmed entities, relationships, constraints, ownership rules, and migrations will be documented here after the project requirements are translated into tested Django designs.

## Application architecture

The application architecture has not yet been established. This section will document the Django project and app structure, responsibilities, data flow, authorization boundaries, payment flow, and important design decisions as implementation develops.

## Routes

No application routes currently exist. Implemented routes, permissions, protected resources, and their user journeys will be recorded here after Django development begins.

## Technology stack

The confirmed project context is a Python and Django full-stack application. Specific framework versions, packages, frontend technologies, payment configuration, database configuration, and hosting choices have not yet been selected or implemented; decisions will be recorded with their rationale.

## Local setup

Local setup instructions, dependency installation, environment variables, and safe Stripe test-mode configuration will be added after the Django project and dependency definitions exist. Until then, there is no runnable application setup to document.

## Testing

No test suite currently exists. Implementation work will follow strict test-driven development: Red, Green, then Refactor. Planned evidence includes unit, integration, permission, payment-state, and browser tests; commands and results will be added only when they exist.

## Deployment

SkillSeat has not been deployed. Deployment targets, production configuration, release steps, and verification evidence will be documented after they are decided and tested.

## Security

Secrets, credentials, local databases, environment files, uploads, and generated deployment artefacts must not enter Git history. The repository `.gitignore` provides the initial protection for local development. The final security review will include server-side authorization, payment-state protection, dependency considerations, and Git-history secret scanning.

## Accessibility

Accessibility requirements, responsive implementation decisions, and manual or automated evidence will be recorded here. No accessibility verification has been completed yet.

## Limitations

The project is not yet implemented. Consequently, there are currently no completed features, test results, deployment outcomes, screenshots, or production claims to report. Future limitations will be recorded honestly as the real scope and evidence develop.

## Credits

SkillSeat is a Code Institute Milestone Project 4 repository. Third-party resources, libraries, design assets, and learning references will be credited here when they are used.

## Reflection

Development reflections, significant decisions, challenges, solutions, and lessons learned will be added throughout the project rather than reconstructed at the end.
