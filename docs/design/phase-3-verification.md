# Phase 3 design and browser verification

## Planning and implementation

[Original wireframes](phase-3-wireframes.md) were committed in `525cfb1` before models/views/templates were implemented. They cover discovery → detail → booking, account/payment status, owner studio and narrow-screen behaviour. These structured planning artefacts are distinct from the real screenshots below.

The implementation retains the planned card discovery, detail/sidebar layout, own-booking dashboard and separate owner studio. System typography, cream paper, deep teal and a warm ticket illustration establish the visual identity without remote fonts or a frontend framework. The landing page adds an original CSS ticket illustration and three-step journey. At <=800px, detail columns stack; <=600px, navigation wraps and cards become one column. The owner screen uses sequential form/roster/resource sections instead of a dense table for mobile use.

Browser findings changed the design: resource form IDs initially duplicated workshop IDs, so labels targeted the wrong field; the form now uses distinct IDs. Password guidance now uses a block help container with programmatic description references. Full/started workshops explain unavailability, existing attendees are sent to booking management, and review actions appear only when eligible. A redundant decorative caption overlapped the ticket and was removed before the final home captures.

## Real screenshots

Captured from the running Django application on 17 October 2026, using the browser tool. All workshop/account data shown is fictional. No generated mockup is represented as a working screenshot. Some captures show earlier checkpoints during the same verification session (for example the payment screen's five-minute guidance was subsequently tightened to four minutes to preserve the provider's minimum remaining time).

| Journey | Actual capture |
| --- | --- |
| Public desktop home | [Desktop](final/home-desktop.jpg) |
| Public mobile home | [390px mobile](final/home-mobile.jpg) |
| Workshop discovery | [Mobile](final/discovery-mobile.jpg), [768px tablet](final/discovery-tablet.jpg) |
| Published workshop detail | [Tablet](final/detail-tablet.jpg) |
| Registration with password guidance | [Mobile](final/register-mobile.jpg) |
| Free booking confirmed | [Mobile](final/booking-confirmed-mobile.jpg) |
| Paid hold with Stripe configuration feedback | [Tablet](final/payment-unconfigured-tablet.jpg) |
| Owner listing/resource management | [Tablet](final/owner-edit-tablet.jpg) |

![Actual SkillSeat desktop home](final/home-desktop.jpg)

## Browser journeys executed

- Anonymous home → workshop discovery → published detail; fictional host, schedule, GBP/free price and seats displayed.
- Registration with a fictional local attendee → success message → sign-in → own account dashboard.
- Free workshop reservation → Confirmed → cancellation → Cancelled.
- Paid workshop reservation → Pending with expiry → Checkout initiation without configured key → honest configuration error; status remained Pending. No external charge or payment success is claimed.
- A controlled local permission grant enabled owner studio → create fictional workshop with UTC dates/capacity/publication → saved owner edit/roster/resource screen. The temporary test permission was revoked and the fictional login disabled after verification.
- Paid test hold cancelled and sign-out verified. Viewport override reset after testing.

## Responsive and accessibility checks executed

The [raw DOM audit](final/browser-dom-audit.json) covers five pages (home, discovery, detail, registration, owner edit) at 320×800, 390×844, 768×1024 and 1280×900. All 20 combinations had one H1/main, no duplicate IDs, no unlabelled input/textarea/select, no missing aria-describedby target, no unnamed buttons and no horizontal overflow. Scroll width was 15px less than viewport width because the desktop browser reserves a scrollbar. This is an automated browser DOM audit, not an axe or WCAG certification.

Keyboard execution verified Enter on Skip to content focuses `main-content` with a visible solid outline, and Tab from Save workshop reaches the next resource input with a solid outline. Forms retain native controls, required/invalid state and associated labels/help/errors. Success/errors use text and role=status, rather than colour alone. Reduced-motion preferences disable smooth scrolling.

[Calculated palette contrast](final/contrast-audit.json), using the actual computed CSS variables and WCAG relative-luminance formula:

| Foreground/background | Ratio |
| --- | ---: |
| Ink #183c36 / paper #f8f7f2 | 11.26:1 |
| White / teal #145f50 | 7.55:1 |
| Muted #4f625a / paper | 6.07:1 |
| Accent/focus #b8431d / paper | 5.07:1 |

These selected normal-text pairs exceed 4.5:1. This does not measure every rendered pixel or every state. Python interface tests cover navigation, viewport metadata, shared styling, labelled resource fields, password descriptions and eligibility feedback. Security tests check escaped user content, CSRF, safe redirects and POST-only actions.

## Limits

No physical touch-device, tablet hardware, screen-reader, full keyboard sweep of every page, axe audit, W3C HTML/CSS validator, browser-engine matrix or complete WCAG 2.2 AA audit was performed. There is no frontend JavaScript to validate. Paid resource download and review eligibility/moderation are verified by Django integration tests with real file responses, not a completed browser payment journey. Genuine Stripe-hosted Checkout and provider-forwarded signed events remain unverified. Phase 4 release validation must broaden these checks after the payment dependency is resolved.
