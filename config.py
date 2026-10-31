"""PromptFix configuration.

Edit these values to wire up monetization. No secrets or API keys
belong in this file -- the Stripe value is just a public payment link.
"""

# HTML pasted verbatim into the ad slot on the page. Replace the
# placeholder with your ad network's snippet (e.g. AdSense ad unit code).
AD_SLOT_HTML = """<!-- PASTE AD NETWORK CODE HERE -->"""

# Public Stripe payment link for PromptFix Pro ($5 one-time).
# Placeholder until the real link is created; the checkout button on the
# page uses whatever string is here.
STRIPE_PRO_LINK = "https://buy.stripe.com/00weVe5It73H6xC4kzfEk03"
