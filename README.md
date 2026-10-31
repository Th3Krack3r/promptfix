# PromptFix

A free tool that turns a vague prompt into a structured one that gets
good answers out of any AI. Paste a prompt, get back a concise version
and a detailed version built around Role / Task / Context / Constraints /
Output format. Rule-based only — no AI API calls, no dependencies.

## How to run it

Requires Python 3 (standard library only, nothing to install):

```bash
python3 app.py
```

Then open <http://localhost:8000> in a browser.

To use a different port:

```bash
python3 app.py 8899
# or
PORT=8899 python3 app.py
```

## How it works

- `improve.py` — the rule-based engine. It infers a role from keywords
  (code/debugging → software developer, resume/job → career coach,
  essay/school → tutor, and so on; default → helpful expert), infers an
  output format from the request type, and restructures the input into
  Role / Task / Context / Constraints / Output format sections.
- `app.py` — a `http.server` server. Serves the page and a
  `POST /api/improve` endpoint that returns JSON
  (`concise`, `detailed`, `role`, `word_count`, plus a `note` and
  clarifying `questions` when the input is under 15 words).
- `index.html` — the single-page UI (inline CSS/JS, no build step).
- `config.py` — monetization settings (see below).

## How to paste ad code

Edit `config.py` and replace the `AD_SLOT_HTML` value with your ad
network's snippet (for example, an AdSense ad unit). It is pasted
verbatim into the ad slot div on the page. The placeholder HTML comment
in the page marks the spot.

## How to set the Stripe link

Edit `config.py` and set `STRIPE_PRO_LINK` to your real Stripe payment
link for the $5 one-time PromptFix Pro purchase. The Pro checkout
button on the page uses that value. It currently points at a placeholder
(`https://example.com/replace-with-stripe-link`) and must be replaced
before launch.

## Monetization note

Two revenue streams, both with near-zero marginal cost since the tool
uses no paid APIs:

1. **Ads** — the free tool page carries an ad slot. This pays per
   visitor, so it grows with traffic, not with usage.
2. **PromptFix Pro ($5 one-time)** — unlimited saved prompts and prompt
   history. The paid tier is where the real short-term income is: a
   cheap one-time purchase converts far faster than ad revenue alone.

The free tool is the marketing: every improved prompt is shareable,
and the "before/after" result is the demo.
