# S1 — Landing page plan (English)

Working name below: **Verivoy** (replace everywhere once the name is final).

## Promise (hero, one sentence)
> **The AI travel agent that never makes things up — and stays with you from takeoff to touchdown.**

Sub-line: *Every place, opening hour and flight status is checked against live sources. Honest prices. Cancel in one click.*

## 3 benefits
1. **Verified, not invented** — Every place is checked (it exists, it's open that day), with real travel times.
   Each item shows a "Verified" or "Not verified" badge. Visa info = official links only.
2. **Share with one link** — Friends and family open the itinerary without creating an account.
   Forward your booking emails; duplicates are detected automatically.
3. **A copilot when things go wrong** — Delay, gate change or cancellation alerts, a plan B, and a ready-to-send
   refund claim template.

Plus an **honest pricing strip** (answers the #1 complaint): Free / Trip Pass ~$9.99 per trip / Plus ~$9.99 per month or
~$79 per year, "cancel in one click, no trial trap". Prices read from config, not hard-coded in copy.

## Page structure
1. Hero: promise + email field + "Join the waitlist" + secondary "Pre-order founder pass" button
2. "Other apps vs. us" — 5 rows (subscription traps, invented places, painful group sharing, flaky import, no help on the road)
3. 3 benefits (cards with a mock "Verified" badge)
4. Pricing strip (honest pricing)
5. Pre-order block (founder offer) + FAQ (when does it launch? Dec 1, 2026 — web, iOS, Android; can I get a refund? yes)
6. Footer: privacy policy, terms, contact

## Waitlist — Supabase schema (PROPOSAL, awaiting validation)

```sql
create extension if not exists citext;

-- One row per email.
create table public.waitlist_signups (
  id               uuid primary key default gen_random_uuid(),
  email            citext not null unique,
  visitor_id       uuid not null,               -- random id stored in the browser, links to landing_events
  locale           text,                        -- navigator.language
  utm_source       text,
  utm_medium       text,
  utm_campaign     text,
  referrer         text,
  marketing_consent boolean not null default false,
  created_at       timestamptz not null default now()
);

-- Funnel events, needed for the 13/10 checkpoint (200 signups, 5% pre-order clicks).
create table public.landing_events (
  id          bigint generated always as identity primary key,
  visitor_id  uuid not null,
  event_type  text not null check (event_type in ('page_view','waitlist_submit','preorder_click','checkout_completed')),
  utm_source  text,
  utm_campaign text,
  created_at  timestamptz not null default now()
);

alter table public.waitlist_signups enable row level security;
alter table public.landing_events  enable row level security;

-- Anonymous visitors may INSERT only. No SELECT/UPDATE/DELETE for anon → emails cannot be read or enumerated.
create policy "anon can join waitlist" on public.waitlist_signups
  for insert to anon with check (true);
create policy "anon can log events" on public.landing_events
  for insert to anon with check (event_type <> 'checkout_completed');   -- that one only comes from the Stripe webhook later
```

Checkpoint query (run in Supabase SQL editor):
```sql
select
  (select count(*) from waitlist_signups)                                               as signups,
  (select count(distinct visitor_id) from landing_events where event_type='page_view')      as visitors,
  (select count(distinct visitor_id) from landing_events where event_type='preorder_click') as preorder_clickers;
```
**Question to settle:** is "5 % de clics" measured on *visitors* or on *signups*? Both are computable; I propose visitors.

## Pre-order — Stripe
- S1 approach: a **Stripe Payment Link** (created in the Stripe dashboard, no backend, no secret key in the app).
  The link URL is public; it lives in `VITE_STRIPE_PREORDER_URL`.
- The button appends `?client_reference_id=<visitor_id>&prefilled_email=<email>` so payments can be matched to signups.
- Suggested offer (to decide): **Founder pass — 1 year of Plus for $49 instead of $79, fully refundable until launch.**
  Stating "refundable" matches the honesty positioning and reduces chargeback risk on a product not yet delivered.
- Later (S5): Supabase Edge Function `stripe-webhook` (secret `STRIPE_WEBHOOK_SECRET` in Supabase secrets) writes
  `checkout_completed`. Not needed for S1: the Stripe dashboard is enough.

## Compliance minimum (international launch)
- Unchecked marketing-consent checkbox (GDPR), privacy policy page listing Supabase + Stripe as processors.
- No third-party trackers before consent; the first-party `landing_events` table is enough for S1.

## API cost
Landing page has no LLM/Places calls → $0 per visitor. Per-trip cost tracking starts in S2 (planned table `api_usage`).
