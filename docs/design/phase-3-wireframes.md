# SkillSeat planning wireframes — before implementation

17 October 2026. Structured low-fidelity wireframes, not screenshots.

## Discovery → detail → booking

```text
DESKTOP (wide)
┌ SkillSeat ─ Workshops ─ My bookings ─ Owner studio ─ Account ┐
│ LEARN SOMETHING WORTH SHARING                               │
│ Practical workshops. A place for your next step.             │
│ [Browse workshops ↓]                                        │
├ Upcoming workshops ─────────────────────────────────────────┤
│ [Date / Title / Owner / Price / Seats / View workshop] × 3   │
└ Clear footer / test payment notice ─────────────────────────┘

DETAIL
┌ Workshop title / description ──── Schedule / price / seats ┐
│ About your host                  [Reserve a place]          │
│ Resources (authorization)        Sign in prompt if needed   │
│ Reviews / attendance policy                                 │
└────────────────────────────────────────────────────────────┘
```

## Account → booking → payment status

```text
┌ My bookings ────────────────────────────────────────────────┐
│ Workshop / date / confirmed or pending / expiry              │
│ [Pay with Stripe test mode] [Cancel booking]                 │
│ Verified paid → resource download; attended → review form    │
└────────────────────────────────────────────────────────────┘
Registration/account: single-column labelled form, errors adjacent
to fields, password help, explicit submit and success feedback.
Return from Checkout: display server state; never confirm from URL.
```

## Owner studio

```text
┌ Your workshops ───────────────────────── [Create workshop] ┐
│ Title / draft or published / reserved vs capacity / Edit    │
├ Edit listing ──────────────────────────────────────────────┤
│ Labelled title, description, location, start/end, price,     │
│ capacity, publication checkbox / [Save workshop]             │
│ Booking roster / attendance action / refund review flags    │
│ Private resource upload / resource list / remove            │
└────────────────────────────────────────────────────────────┘
```

## Narrow screens and accessibility intent

Navigation wraps naturally; cards and detail columns become one column. Forms use full-width fields, visible labels, 44px controls, visible focus and a skip link. No hover-dependent actions. Cream background, dark ink, deep teal actions and orange accents establish a warm learning identity. System typography avoids third-party requests. Errors and payment status use words as well as colour. Semantic headings, landmarks and native controls support keyboard use.
