# Visibility Phase 1: decisions and open items

Prepared 2026-10-07 on top of `main` after PRs #13 and #14, updated by the remediation pass the same day. Internal; `docs/` is excluded from deploys.

## What matters, and what is only housekeeping

**Important / meaningful (these are the point of Phase 1)**

- Product truth: the public site describes only what the product does today (Free) and labels SteadFolio+ and broker connection as planned.
- Accurate, consistent entity definition across homepage, About, FAQ, pricing, meta/OG, JSON-LD and `llms.txt`.
- Author accountability: articles are published by "The SteadFolio Team"; About names the founder/editor, states the operator per the Terms, and explains what a review date means.
- Source quality and honest review/update dates (no `datePublished`, review dates only where claims were checked).
- Article and BreadcrumbList structured data that matches the visible page.
- Canonicals, crawlability, indexability, sitemap accuracy.
- Internal linking (audited only in this pass, see below).
- Authoritative references on factual claims (EUR-Lex, ECB, Eurostat, NBER, official broker pages).
- Useful original content (nothing new was added in Phase 1).

**Useful semantic housekeeping, not major Google visibility levers**

- **FAQPage schema.** Kept because it matches the visible FAQ text and costs nothing. It is not a current Google rich-result opportunity: Google limited FAQ rich results to well-known government and health sites in 2023. Do not expect search appearance or ranking gains from it. `scripts/check_site.py` checks that every FAQ question in the schema is visible on the page.
- **`llms.txt`.** Kept as a plain-text site guide. It is experimental and ecosystem-specific: it is not a documented Google ranking factor, Google AI Overviews signal or proven GEO mechanism, and some AI tools may ignore it. It describes the site; it does not replace crawlable, well-sourced pages.

## Rules used

- **Dates.** No `datePublished` anywhere: real publication dates are not recorded in the repo. "Last reviewed: October 7, 2026" and `dateModified: 2026-10-07` appear only on 13 articles whose claims were individually checked in this pass (arithmetic recomputed, or the claim confirmed against official-domain search results). The other 33 older articles carry no date. `about.html` says what a review date means.
- **Authorship.** Article author stays the organisation, "The SteadFolio Team". `about.html` has a restrained founder/editor section (Andreas Broutas, Founder & Editor). No article carries a named personal reviewer, because no named human review has taken place.
- **Sources.** Only primary or authoritative sources, only where they back a specific claim. The sandbox could not open EUR-Lex, ECB, ESMA or broker sites directly; claims were confirmed through search results from the official domains, and the owner should spot-check the new links.
- **Pricing.** SteadFolio+ is shown as planned and not purchasable, with no price. The planned €9.99 / €89.90 figures are deliberately not published.
- **Structured data restraint.** No Review, AggregateRating, FinancialProduct, InvestmentOrDeposit, Person or third-party-rating markup. The Trustpilot profile (confirmed live by the owner) stays in the Organization `sameAs` as an entity link only; no Trustpilot rating or review data is in markup. `founder` is not in the Organization JSON-LD because the homepage does not show it.

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

## Remediation pass

- **Broker sources.** DEGIRO links its official Greek pages (`degiro.gr`: costs overview, ETF Core Selection, who supervises DEGIRO) instead of `degiro.com/uk`. The legal entity is "flatexDEGIRO Bank SE". The connectivity fee is described as 0.25% of account value, capped at €2.50 per exchange per calendar year, not charged on the domestic market (Athens Stock Exchange for Greek clients) or on Tradegate Core Selection ETFs. No Fair Use Policy wording remains on the site: the Greek Core Selection page says that policy has been removed. Trading 212 no longer says "Invest and ISA accounts" (ISA is UK-only), links entity-specific official pages, and treats Greece as served by Trading 212 Markets Ltd (CySEC); "Trading 212 Ltd (FSC, Bulgaria)" was removed from the Greece-facing regulatory summary.
- **Verification dates.** Scoped, not global: DEGIRO ETF costs, connectivity and FX fees and legal entity, and Trading 212 commission, custody, FX fee and regulating entity, are marked verified 2026-10-07; all other broker figures keep 2026-08-11 (the `LAST_VERIFIED` constant is unchanged). The checks were made against official-domain search results, because the sandbox could not open broker pages.
- **Founder / accountability.** New "Who is behind SteadFolio" section on `about.html`. No credentials, adviser or regulated status is claimed. The operator disclosure stays in the Terms and Privacy Policy only.
- **Product-claim regression audit.** Two wording problems of our own were fixed on `pricing.html`: "limited daily quota" (the owner brief says only "limited quota") and "Personalized news for your holdings" (now "Personalized news").

## Needs the owner

- **DEGIRO stock commissions and a few statements are not re-verified.** Search results for the Greek fee pages disagree with the page's "€2-4.90 per trade, varies by exchange" (they point to €0.50 plus a €1 handling fee for Athens-listed shares and €3.90 plus €1 for European shares, but may reflect an older fee table), so the figure was left unchanged and carries the 2026-08-11 date. "No fractional shares" and "no savings plan" were not confirmed on a Greek page. The Core Selection wording no longer states a number of ETFs, because the count could not be confirmed.
- **Free-plan wording to confirm against the app:** "Personalized news" (exact Free behaviour), "one financial goal with monthly check-ins", and the "What-If analysis against a benchmark" wording (the old page said one benchmark on Free).
- Page-level OG images are the logo or an app screenshot; dedicated share images would help.
- 33 older articles have no review date and 36 have no sources section. Statistics-bearing ones (S&P 500 history, bull/bear durations, lump sum vs DCA, REITs, pensions) need a human review against sources before they get a date.

## Possible later improvement: `datePublished`

First-commit dates from git span 2026-07-20 to 2026-08-21 and could be reconstructed per article. They are the date a file was first committed, not necessarily the date it was published, so confirm against Vercel deployment history before using them. Not applied.

## Internal linking audit (no links added in the remediation pass)

- 50 English articles; about 154 unique in-text article-to-article links (about 3.1 per article), about 246 including "Read next" and "Continue reading" boxes (about 4.9).
- No article is a true orphan: every one is linked from the blog hub and the sitemap.
- 13 articles have no in-text inbound link from another article. Four have no inbound link from any other article at all (near-orphans, linked only from the blog hub): `esg-sustainable-investing`, `how-to-research-an-investment`, `pension-retirement-accounts`, `what-is-a-reit`. Two more (`feeling-behind-on-investing`, `robo-advisors-vs-learning-yourself`) have a single "Read next" box link. The other seven are reached only through boxes.
- Four articles have no in-text outbound article link: `how-markets-really-work`, `robo-advisors-vs-learning-yourself`, `understanding-fomo-investing`, `what-are-bonds`.
- Poorly connected clusters: the behaviour/psychology set (about 9 articles, linked mainly by boxes), the "specific topics" set (ESG, pensions, REITs, crypto, robo-advisors), and the macro set (inflation, recession, bonds, liquidity). The ETF/UCITS/accumulating/broker cluster is well connected.
- Design the link architecture separately, from user journeys and search intent.

## Check

`python3 scripts/check_site.py [--report]` runs the hard checks (canonicals, noindex, JSON-LD, links and fragments, sitemap, robots, redirects, FAQ schema vs visible text, hreflang) and prints the coverage and claim greps.
