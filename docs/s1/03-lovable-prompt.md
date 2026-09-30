# S1 — Lovable prompt (copy everything inside the block)

Before pasting: (1) validate the schema in `02-landing-plan.md`, (2) replace `Verivoy` if another name is chosen,
(3) connect your own Supabase project in Lovable (Integrations → Supabase) rather than a Lovable-managed database,
(4) create the Stripe Payment Link and put its URL in the env var below.

```text
Build a single-page, mobile-first marketing landing page in ENGLISH for "Verivoy", an AI travel agent app launching December 1, 2026 on web, iOS and Android. Stack: React + TypeScript + Tailwind + shadcn/ui, Supabase (already connected) for the waitlist. All code, comments and identifiers in English.

POSITIONING
"The AI travel agent that never makes things up — and stays with you from takeoff to touchdown." Tone: calm, honest, confident, no hype words ("revolutionary", "magic"). Design: clean, lots of white space, one accent color (deep teal #0F766E), a small green "✓ Verified" pill used as a recurring visual motif. Support dark mode. Inter font. Fast: no heavy images; use simple inline SVG illustrations and a phone mockup built in HTML/CSS showing a day itinerary where each place has a "✓ Verified · Open 9:00–18:00" pill and one item shows a grey "Not verified" pill.

SECTIONS (in order)
1. Header: logo text "Verivoy", anchor links (How it works, Pricing, FAQ), button "Join the waitlist".
2. Hero: H1 = "The AI travel agent that never makes things up." Subtitle = "Every place, opening hour and flight status is checked against live sources — and it stays with you from takeoff to touchdown." Email input + primary button "Join the waitlist" + secondary outline button "Pre-order the Founder Pass". Small line under the form: "Launching December 1, 2026 · Web, iOS & Android · No spam, unsubscribe anytime." Phone mockup on the right (below on mobile).
3. "Why travelers are fed up" comparison table, 2 columns "Other travel apps" vs "Verivoy":
   - Subscription traps, hard to cancel → Honest prices, monthly option, cancel in one click
   - AI invents places and opening hours → Every place checked on live sources, marked Verified or Not verified
   - Group sharing needs everyone to sign up → Share with a simple link, no account needed
   - Booking import misses or duplicates trips → Forward your emails, duplicates detected automatically
   - No help when things go wrong → A copilot during your trip: alerts, plan B, refund claim help
4. Three benefit cards: "Verified, not invented" / "Share with one link" / "A copilot when things go wrong" (use the texts above, 2 lines each).
5. Pricing strip with 3 cards. Read all prices from a single config file src/config/pricing.ts (do not hard-code them in JSX):
   Free ($0: verified planning, link sharing, 1 active trip) / Trip Pass ($9.99 per trip: copilot, flight alerts, refund help) / Plus ($9.99/month or $79/year: unlimited trips). Under it: "No free-trial trap. Cancel in one click." Label prices "Launch prices, subject to change".
6. Founder Pass block: "Pre-order the Founder Pass — 1 year of Plus for $49 instead of $79. Fully refundable until launch." Button "Pre-order for $49". Founder price also comes from src/config/pricing.ts.
7. FAQ (accordion): When does it launch? / Which countries? (worldwide, English first) / How do you verify places? (live data from Google Places and flight-status providers; if something can't be checked we say so) / Do you give visa advice? (No — we link to official government sources only) / Can I get my pre-order refunded? (Yes, anytime before launch, email us) / Is my email shared? (Never sold.)
8. Footer: © 2026 Verivoy, links to /privacy and /terms (create simple placeholder pages with a clear "Draft" notice), contact email placeholder.

WAITLIST (Supabase)
Tables already defined by me (create them with this exact SQL migration if they don't exist):
<paste the SQL block from docs/s1/02-landing-plan.md here>
Behavior:
- On first load, create a random visitor_id with crypto.randomUUID(), store it in localStorage (wrap in try/catch; fall back to an in-memory id), and insert a 'page_view' event with utm_source and utm_campaign read from the URL.
- Waitlist form: validate email client-side; an unchecked checkbox "Send me launch news and tips" maps to marketing_consent. Insert into waitlist_signups with visitor_id, locale (navigator.language), utm_source/utm_medium/utm_campaign, document.referrer. Also insert a 'waitlist_submit' event. Use insert only — never select from these tables in the frontend. If the insert fails with a unique violation (code 23505), show the same success message ("You're on the list! We'll email you before launch.") so emails can't be enumerated. Show a friendly error for other failures.
- Pre-order buttons: insert a 'preorder_click' event, then redirect to import.meta.env.VITE_STRIPE_PREORDER_URL with query params client_reference_id=<visitor_id> and, if the user already typed a valid email, prefilled_email=<email>. If the env var is missing, disable the button and show "Pre-orders open soon".

SECURITY / CONFIG RULES
- No secrets or API keys in code. Only use the Supabase URL and anon/publishable key through the standard env vars, and VITE_STRIPE_PREORDER_URL. Add a .env.example listing the variable names with empty values.
- No third-party analytics or tracking scripts.

QUALITY
- Lighthouse performance and accessibility ≥ 90 on mobile; semantic HTML; visible focus states; labels on inputs.
- SEO: title "Verivoy — The AI travel agent that never makes things up", meta description, Open Graph tags (og:title, og:description), favicon from a simple SVG "V" with a check mark.
- Fully responsive from 360px width, no horizontal scroll.
```
