# Visibility Phase 1: decisions and open items

Prepared 2026-10-07 on top of `main` after PRs #13 and #14. Internal; `docs/` is excluded from deploys.

## Rules used

- **Dates.** No `datePublished` anywhere: real publication dates are not recorded in the repo. "Last reviewed: October 7, 2026" and `dateModified: 2026-10-07` appear only on 13 articles whose claims were individually checked in this pass (arithmetic recomputed, or the claim confirmed against a primary source). The other 33 older articles carry no date. `about.html` says what a review date means.
- **Authorship.** The repo names no person, so the author stays the organisation: "The SteadFolio Team" (the existing model on the reworked articles and the Greek pages). `about.html` states the operator as described in the Terms (an individual based in Greece). Naming a person is a decision for the owner.
- **Sources.** Only primary or authoritative sources, only where they back a specific claim. The sandbox could not open EUR-Lex, ECB or ESMA directly; claims were confirmed through search results from the official domains, and URLs reuse patterns already on the site.
- **Pricing.** SteadFolio+ is shown as planned and not purchasable, with no price. The planned €9.99 / €89.90 figures are deliberately not published.

## Factual corrections made

| Page | Problem | Fix |
|---|---|---|
| `blog-compound-interest-explained` | "€1,074.90 in growth-on-growth" was wrong | Year-2 growth is €74.90, balance €1,144.90, of which €4.90 is growth on growth |
| `blog-saving-vs-investing` | The decision rule was inverted | Rewritten: needing the money within 1-2 years points to savings |
| `blog-how-markets-really-work` | PFOF described as "legal and regulated" | EU prohibits it for retail clients (Reg. (EU) 2024/791); transition ended 30 June 2026 |
| `blog-is-crypto-good-for-beginners` | Crypto described only as "less regulated" | Mentions MiCA and the absence of an investor-compensation scheme |
| `blog-how-to-buy-your-first-etf` | Worked example did not add up (2.24 shares) | €200 less a €1.50 fee at €89 = 2.23 shares |
| `blog-waiting-perfect-time-invest` | Stray text fragment and extra closing tags | Removed |
| `brokers/degiro.html` | `<title>` said "Trading 212" | Now "DEGIRO Review 2026..." |
| `pricing.html`, `faq.html`, `journey.html`, `best-tools-to-learn-investing.html` | Stale Free/Plus and broker-sync claims | See the PR description |

## Not changed, needs the owner

- Trading 212's and DEGIRO's "official source" links point at UK pages (Invest ISA/SIPP fee article; `degiro.com/uk`). Check they are the right regulatory entity for EU readers.
- Trustpilot is in the Organization `sameAs`. Keep it only if that profile is claimed and live.
- The Free list on `pricing.html` carries over Watchlist, Panic Mode, progress and streaks, ETF comparison and proactive-style features from the old page. Confirm they are still Free.
- 33 older articles have no review date and 36 have no sources section. Many are conceptual, but statistics-bearing ones (S&P 500 history, bull/bear durations, lump sum vs DCA, REITs, pensions) need a human review against sources before they get a date.
- Page-level OG images are the logo or an app screenshot; dedicated share images would help.

## Check

`python3 scripts/check_site.py [--report]` runs the hard checks (canonicals, noindex, JSON-LD, links and fragments, sitemap, robots, redirects, FAQ schema vs visible text, hreflang) and prints the coverage and claim greps.
