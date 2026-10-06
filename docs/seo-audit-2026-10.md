# SteadFolio.eu: SEO audit and implementation (October 2026)

Branch: `ccr-7fdf86a9-x24j7g` · Baseline: `origin/main` @ `1fe8b6c` · Prepared 2026-10-06

This document is internal. `docs/` is listed in `.vercelignore` so it is not deployed.

## 0. Scope, method and limits

**How the audit was done.** Every HTML file in the repository was parsed (titles, descriptions, canonicals, robots, hreflang, headings, JSON-LD, Open Graph, images, word counts, internal link graph, sitemap membership). Product claims were checked against the site's own product pages (homepage, pricing, journey, and the Greek ETF guide reviewed on Oct 6). Pages were rendered in headless Chromium at 375px and 1280px.

**What could not be checked from this environment.** The session's network policy blocked:

- the live site `steadfolio.eu` (no live redirect, header or status-code checks),
- the brokers' official sites (traderepublic.com, scalable.capital, revolut.com),
- spglobal.com and esma.europa.eu (sources are cited, but only claims confirmed by search results are used).

There was also no per-URL Search Console data, so the GSC figures in the brief were used as context only. Titles and meta descriptions were changed only where the content changed or the intent was clearly mismatched.

**Rule followed for financial figures:** no new broker fee was introduced. Every figure on the broker pages already existed on the profile or in the `brokers[]` data on `broker-comparison.html` (verified 2026-08-11). New text only does arithmetic on those figures, such as "€1 is 2% of a €50 order".

---

## A. SEO audit report

### A1. Architecture

- Static HTML site on Vercel. There is no build step, package.json, CI or test suite. `vercel.json` has one redirect (`/index.html` → `/`) and content-type headers.
- 85 HTML files:
  - 11 core pages (home, about, blog, FAQ, pricing, journey, broker comparison, learning-tools comparison, 3 legal),
  - 50 English articles (`/blog-*.html`),
  - 10 broker profiles (`/brokers/*.html`),
  - 4 Greek pages (`/el/`),
  - **10 legacy root broker duplicates** (`/trade-republic.html` etc.).
- Content is server-rendered static HTML everywhere except `broker-comparison.html`, where all comparison content was injected by JavaScript.
- Tracking: GA4 `G-V3SFS38ZZL` and Microsoft Clarity, both loaded only after consent by `js/cookie-consent.js`. `js/cta-tracking.js` sends a consent-gated `cta_click` event for links with `data-sf-cta`. `js/utm-forward.js` forwards UTM parameters to the app. Bing verification uses `a212012d8b844af8997798ca9d3907a9.txt`. robots.txt allows everything and lists the sitemap. `llms.txt` exists.

### A2. Audit matrix: confirmed issues

| # | Issue | Affected URLs | Severity | Evidence | Fix | Status |
|---|---|---|---|---|---|---|
| 1 | Broker profiles had no static inbound links; they were reachable only through `reviewUrl` links injected by JS | all 10 `/brokers/*.html` | High | Static link graph: 0 inbound links each | Cross-links on every profile, static summary table, "Choose a Broker" path | **Fixed** (now 9–11 static inbound links each) |
| 2 | Comparison content was JS-only. Static HTML had the filter chips and headings but no broker data. FAQPage schema described questions not visible on the page | `/broker-comparison.html` | High | ~238 words of static text; FAQ questions absent from visible text | Pre-rendered cards (identical to JS output), static summary table re-rendered from `brokers[]`, guide, visible FAQ | **Fixed** |
| 3 | Index fund guide was thin (~490 words, "2 min read"), with no canonical, schema or sources. Its H1 said "Why Do People **Recommend** Them?", at odds with the no-recommendation positioning | `/blog-what-is-index-fund.html` | High (priority page) | Page source | Full rewrite (see B) | **Fixed** |
| 4 | Broker fees may be out of date. Third-party sites (not official) report Scalable Capital pricing changes from 2026-09-01 and changes to Revolut's trading-fee model after the 2026-08-11 verification | broker comparison, Scalable Capital and Revolut profiles (possibly others) | High (YMYL accuracy) | Web search results only; official sites blocked from this environment | **Not changed.** Needs human re-verification against official pages | **Open: human action** |
| 5 | 64 indexable pages had no canonical tag | see inventory | Medium | Parsed `<head>` | Self-referencing canonical added | **Fixed** |
| 6 | FAQPage JSON-LD did not match visible FAQ. Four articles carried the "Is investing gambling?" questions copied from another page, and the gambling article's 4th question differed from its visible FAQ | `/blog-betting-20-vs-investing-20.html`, `/blog-investing-50-a-month.html`, `/blog-psychology-quick-money.html`, `/blog-waiting-perfect-time-invest.html`, `/blog-is-investing-gambling.html` | Medium | Schema vs visible-text comparison | Schema rebuilt from each page's visible FAQ | **Fixed** |
| 7 | Six published, linked articles missing from sitemap.xml | `/blog-how-to-buy-your-first-etf.html`, `/blog-is-investing-gambling.html`, `/blog-investing-50-a-month.html`, `/blog-betting-20-vs-investing-20.html`, `/blog-psychology-quick-money.html`, `/blog-waiting-perfect-time-invest.html` | Medium | Sitemap vs files | Added | **Fixed** |
| 8 | Ten legacy root broker pages duplicate `/brokers/*` (same content, older nav). They have no canonical, aren't in the sitemap and aren't linked, but any external or legacy link would index a duplicate | `/degiro.html`, `/etoro.html`, `/freedom24.html`, `/interactive-brokers.html`, `/lightyear.html`, `/revolut.html`, `/scalable-capital.html`, `/trade-republic.html`, `/trading-212.html`, `/xtb.html` | Medium | `diff` against `/brokers/*` | Proposal: 301 to `/brokers/*` and delete the files (see C, P1) | **Open: decision** (removal was declined in-session) |
| 9 | Inaccurate product claim: the ETF guide said the ETF Evaluator "walks you through these same seven checks on a real portfolio". No product page supports this | `/blog-how-to-evaluate-etf.html` | Medium (trust) | Homepage, journey and Greek ETF guide descriptions | Replaced with the description from the reviewed Greek guide | **Fixed** |
| 10 | 37 older articles ended without any related-reading or next-step link (1–3 contextual links in total) | see B3 | Medium | Link counts | Four learning paths on the blog plus a "Read next" box | **Fixed** |
| 11 | Author and editorial transparency is thin: articles are by "The SteadFolio Team", no person is named anywhere, and there was no sourcing or corrections information | site-wide, `/about.html` | Medium (E-E-A-T) | Repository contains no author details | About page now has "How we write our guides" (evidenced practices only) | **Partly fixed**; names and credentials need a human |
| 12 | 566 internal links pointed at `/index.html`, which 301-redirects to `/` | all English pages | Low | `vercel.json` plus hrefs | Rewritten to `/` (fragments kept) | **Fixed** (Greek pages untouched) |
| 13 | Organization schema logo `steadfolio-icon-1080.png` doesn't exist in the repo | `/` | Low | File missing | Points to `logo-icon.png` (270×240) | **Fixed** (see TODO on a dedicated logo) |
| 14 | Horizontal overflow at 375px from wide tables | `/best-tools-to-learn-investing.html`, `/blog-investing-50-a-month.html` | Low | Playwright `scrollWidth` check, also on main | Tables wrapped in `overflow-x:auto` | **Fixed** |
| 15 | No Open Graph or Twitter tags on English pages (only the Greek pages had them) | 81 pages | Low | Parsed `<head>` | Added on the 6 priority/hub pages changed here | **Partly fixed** |
| 16 | Article and Breadcrumb schema on only 3 English articles; no `datePublished` anywhere | most articles | Low | Parsed JSON-LD | Added on the index fund guide and broker profiles | **Partly fixed** |
| 17 | Brand written two ways, "Steadfolio" and "SteadFolio" | 39 pages | Low | grep | Fixed on the index fund page only | Backlog |
| 18 | Short or generic core titles: About (18 chars), Blog (17), FAQ (16), Pricing (20). Homepage description is 232 chars and will be truncated | `/about.html`, `/blog.html`, `/faq.html`, `/pricing.html`, `/` | Low | Parsed `<title>` | Not changed: the homepage drives most clicks and per-query data is needed first | Backlog |
| 19 | Heading level skips (H2 → H4 style) | `/cookie-policy.html`, `/journey.html` | Low | Heading parse | Not changed | Backlog |
| 20 | `/brokers/*` pages load `cookie-consent.js` without `data-clarity="1"`, so Clarity never loads there, unlike most pages | `/brokers/*` | Info | Script tag diff | **Not changed** (tracking is out of scope) | Decision for owner |

### A3. Checked and found OK

- **Hreflang:** EN↔EL pairs (`what-is-an-etf`↔`ti-einai-etf`, `what-is-the-sp-500`↔`ti-einai-sp-500`, `how-to-start-investing`↔`ependyseis-gia-arxarious`) are reciprocal, self-referencing, and have `x-default`. `/el/` has no English equivalent, which is correct.
- **robots.txt** allows all crawlers and declares the sitemap. No `noindex` anywhere.
- **Headings:** exactly one H1 on every page.
- **Images:** every `<img>` has alt text (the Greek pages have one decorative empty alt).
- **Rendering:** all articles and profiles are fully static HTML.
- **Consent:** GA4 and Clarity load only after consent.

### A4. Content weaknesses

- **Thin articles.** 18 articles have under about 500 words of body text, for example `robo-advisors-vs-learning-yourself` (395), `understanding-fomo-investing` (403), `setting-a-financial-goal` (408), `what-are-bonds` (414) and `what-is-asset-allocation` (434). Most have no sources, no review date and no FAQ.
- **Weak CTAs.** Older articles end with a generic "Start learning with Sofia" CTA that isn't matched to what the reader came for, and isn't measured (no `data-sf-cta`).
- **Broker profiles.** The seven non-priority profiles still use the short template: fees table, pros and cons, 3 FAQs.
- **Few sources.** Primary sources appear mainly on the Sept–Oct reworked pages and the Greek guides.

### A5. Priority ranking of opportunities

1. Keep the broker data correct: re-verify fees, update `LAST_VERIFIED`, and keep profiles in sync. YMYL accuracy is the trust foundation of the "Choose a Broker" cluster.
2. Use per-URL GSC data (query × page) to rewrite titles and descriptions for pages that get impressions but no clicks. Start with the broker profiles and the ETF articles named in the brief.
3. Bring the remaining seven broker profiles and the thinnest "Understand ETFs" articles up to the new template.
4. Measure activation: register `cta_id`/`page_language`/`link_url` as GA4 custom dimensions and connect `cta_click` to app sign-up across domains.
5. Add real author and reviewer attribution (only real people with real credentials).

### A6. URL inventory (all discoverable public HTML pages, after this branch)

- "Inbound internal" counts unique pages linking to the URL in static HTML.
- The homepage's "0 → 70" happens because links previously pointed at `/index.html`, a different URL that redirects.
- Word counts exclude header, nav and footer.

| URL | Type | Title len | Desc len | Canonical (before → after) | JSON-LD (after) | Words | Inbound internal (before → after) | Sitemap | Changed |
|---|---|---|---|---|---|---|---|---|---|
| `/about.html` | Core | 18 | 129 | ✗ → ✓ | — | 433 | 84 → 84 | ✓ | ✓ |
| `/best-tools-to-learn-investing.html` | Core | 70 | 178 | ✗ → ✓ | FAQPage | 1902 | 71 → 71 | ✓ | ✓ |
| `/blog.html` | Core | 17 | 147 | ✗ → ✓ | — | 1718 | 84 → 84 | ✓ | ✓ |
| `/broker-comparison.html` | Core | 61 | 174 | ✗ → ✓ | FAQPage | 1328 | 81 → 81 | ✓ | ✓ |
| `/cookie-policy.html` | Core | 26 | 138 | ✓ → ✓ | — | 871 | 84 → 84 | ✓ | ✓ |
| `/faq.html` | Core | 16 | 133 | ✗ → ✓ | FAQPage | 728 | 84 → 84 | ✓ | ✓ |
| `/` | Core | 58 | 232 | ✗ → ✓ | Organization;WebApplication | 1367 | 0 → 70 | ✓ | ✓ |
| `/journey.html` | Core | 65 | 169 | ✗ → ✓ | — | 824 | 75 → 75 | ✓ | ✓ |
| `/pricing.html` | Core | 20 | 142 | ✗ → ✓ | — | 354 | 84 → 84 | ✓ | ✓ |
| `/privacy.html` | Core | 27 | 94 | ✗ → ✓ | — | 743 | 84 → 84 | ✓ | ✓ |
| `/terms.html` | Core | 29 | 71 | ✗ → ✓ | — | 446 | 84 → 84 | ✓ | ✓ |
| `/blog-accumulating-vs-distributing-etfs.html` | Article | 70 | 134 | ✗ → ✓ | FAQPage | 816 | 5 → 8 | ✓ | ✓ |
| `/blog-beginner-investing-mistakes.html` | Article | 65 | 160 | ✗ → ✓ | — | 500 | 3 → 3 | ✓ | ✓ |
| `/blog-behavior-matters-more-than-strategy.html` | Article | 67 | 153 | ✗ → ✓ | — | 444 | 4 → 8 | ✓ | ✓ |
| `/blog-betting-20-vs-investing-20.html` | Article | 65 | 147 | ✗ → ✓ | FAQPage | 698 | 4 → 4 | ✓ | ✓ |
| `/blog-building-an-investing-habit.html` | Article | 70 | 123 | ✗ → ✓ | — | 442 | 1 → 8 | ✓ | ✓ |
| `/blog-bull-vs-bear-market.html` | Article | 63 | 150 | ✗ → ✓ | FAQPage | 850 | 3 → 5 | ✓ | ✓ |
| `/blog-compound-interest-explained.html` | Article | 53 | 156 | ✗ → ✓ | — | 457 | 8 → 8 | ✓ | ✓ |
| `/blog-dollar-cost-averaging.html` | Article | 48 | 141 | ✗ → ✓ | — | 568 | 15 → 22 | ✓ | ✓ |
| `/blog-emergency-fund-before-investing.html` | Article | 65 | 159 | ✓ → ✓ | BreadcrumbList;FAQPage;Article | 2630 | 16 → 17 | ✓ | ✓ |
| `/blog-esg-sustainable-investing.html` | Article | 70 | 145 | ✗ → ✓ | FAQPage | 769 | 1 → 1 | ✓ | ✓ |
| `/blog-etf-domicile-withholding-tax.html` | Article | 82 | 137 | ✗ → ✓ | FAQPage | 855 | 4 → 8 | ✓ | ✓ |
| `/blog-feeling-behind-on-investing.html` | Article | 74 | 144 | ✗ → ✓ | — | 432 | 1 → 2 | ✓ | ✓ |
| `/blog-how-markets-really-work.html` | Article | 65 | 155 | ✗ → ✓ | — | 555 | 2 → 3 | ✓ | ✓ |
| `/blog-how-much-money-to-start-investing.html` | Article | 59 | 151 | ✓ → ✓ | BreadcrumbList;FAQPage;Article | 2150 | 11 → 12 | ✓ | ✓ |
| `/blog-how-to-buy-your-first-etf.html` | Article | 75 | 165 | ✗ → ✓ | FAQPage | 1505 | 7 → 9 | ✓ | ✓ |
| `/blog-how-to-choose-a-broker.html` | Article | 51 | 123 | ✗ → ✓ | — | 532 | 6 → 18 | ✓ | ✓ |
| `/blog-how-to-evaluate-etf.html` | Article | 70 | 156 | ✓ → ✓ | BreadcrumbList;FAQPage;Article | 2586 | 19 → 21 | ✓ | ✓ |
| `/blog-how-to-research-an-investment.html` | Article | 83 | 117 | ✗ → ✓ | — | 456 | 1 → 1 | ✓ | ✓ |
| `/blog-how-to-start-investing.html` | Article | 71 | 146 | ✓ → ✓ | FAQPage | 976 | 5 → 9 | ✓ | ✓ |
| `/blog-hysa-vs-investing.html` | Article | 78 | 142 | ✗ → ✓ | FAQPage | 798 | 2 → 4 | ✓ | ✓ |
| `/blog-investing-50-a-month.html` | Article | 51 | 140 | ✗ → ✓ | FAQPage | 601 | 5 → 7 | ✓ | ✓ |
| `/blog-investing-in-your-20s.html` | Article | 56 | 145 | ✗ → ✓ | FAQPage | 734 | 1 → 3 | ✓ | ✓ |
| `/blog-investing-takes-time.html` | Article | 69 | 168 | ✗ → ✓ | — | 541 | 1 → 3 | ✓ | ✓ |
| `/blog-is-crypto-good-for-beginners.html` | Article | 68 | 143 | ✗ → ✓ | — | 459 | 2 → 2 | ✓ | ✓ |
| `/blog-is-investing-gambling.html` | Article | 72 | 154 | ✗ → ✓ | FAQPage | 1623 | 5 → 6 | ✓ | ✓ |
| `/blog-lump-sum-vs-dollar-cost-averaging.html` | Article | 51 | 166 | ✗ → ✓ | — | 476 | 2 → 3 | ✓ | ✓ |
| `/blog-pension-retirement-accounts.html` | Article | 62 | 140 | ✗ → ✓ | FAQPage | 780 | 1 → 1 | ✓ | ✓ |
| `/blog-psychology-quick-money.html` | Article | 69 | 141 | ✗ → ✓ | FAQPage | 655 | 4 → 6 | ✓ | ✓ |
| `/blog-robo-advisors-vs-learning-yourself.html` | Article | 62 | 151 | ✗ → ✓ | — | 395 | 1 → 2 | ✓ | ✓ |
| `/blog-rule-of-72.html` | Article | 76 | 153 | ✗ → ✓ | FAQPage | 913 | 2 → 2 | ✓ | ✓ |
| `/blog-saving-vs-investing.html` | Article | 61 | 123 | ✗ → ✓ | — | 441 | 3 → 5 | ✓ | ✓ |
| `/blog-setting-a-financial-goal.html` | Article | 72 | 143 | ✗ → ✓ | — | 408 | 5 → 7 | ✓ | ✓ |
| `/blog-stock-market-crash.html` | Article | 54 | 147 | ✗ → ✓ | FAQPage | 767 | 3 → 7 | ✓ | ✓ |
| `/blog-understanding-fomo-investing.html` | Article | 49 | 136 | ✗ → ✓ | — | 403 | 5 → 6 | ✓ | ✓ |
| `/blog-understanding-market-volatility.html` | Article | 70 | 136 | ✗ → ✓ | — | 482 | 7 → 10 | ✓ | ✓ |
| `/blog-understanding-risk-tolerance.html` | Article | 46 | 171 | ✗ → ✓ | — | 464 | 5 → 9 | ✓ | ✓ |
| `/blog-waiting-perfect-time-invest.html` | Article | 82 | 161 | ✗ → ✓ | FAQPage | 922 | 3 → 5 | ✓ | ✓ |
| `/blog-what-are-bonds.html` | Article | 52 | 139 | ✗ → ✓ | — | 414 | 3 → 4 | ✓ | ✓ |
| `/blog-what-are-dividends.html` | Article | 54 | 152 | ✗ → ✓ | FAQPage | 847 | 2 → 3 | ✓ | ✓ |
| `/blog-what-are-ucits-etfs.html` | Article | 67 | 134 | ✗ → ✓ | FAQPage | 874 | 6 → 8 | ✓ | ✓ |
| `/blog-what-is-a-recession.html` | Article | 67 | 138 | ✗ → ✓ | FAQPage | 730 | 2 → 2 | ✓ | ✓ |
| `/blog-what-is-a-reit.html` | Article | 64 | 130 | ✗ → ✓ | FAQPage | 776 | 1 → 1 | ✓ | ✓ |
| `/blog-what-is-a-stock.html` | Article | 66 | 146 | ✗ → ✓ | FAQPage | 929 | 4 → 5 | ✓ | ✓ |
| `/blog-what-is-an-etf.html` | Article | 68 | 142 | ✓ → ✓ | FAQPage | 1153 | 6 → 10 | ✓ | ✓ |
| `/blog-what-is-asset-allocation.html` | Article | 43 | 149 | ✗ → ✓ | — | 434 | 3 → 7 | ✓ | ✓ |
| `/blog-what-is-diversification.html` | Article | 42 | 145 | ✗ → ✓ | — | 500 | 6 → 13 | ✓ | ✓ |
| `/blog-what-is-index-fund.html` | Article | 63 | 162 | ✗ → ✓ | BreadcrumbList;Article;FAQPage | 2180 | 8 → 8 | ✓ | ✓ |
| `/blog-what-is-inflation.html` | Article | 72 | 137 | ✗ → ✓ | FAQPage | 816 | 2 → 2 | ✓ | ✓ |
| `/blog-what-is-liquidity.html` | Article | 36 | 139 | ✗ → ✓ | — | 460 | 2 → 2 | ✓ | ✓ |
| `/blog-what-is-the-sp-500.html` | Article | 52 | 159 | ✓ → ✓ | FAQPage | 1145 | 4 → 5 | ✓ | ✓ |
| `/brokers/degiro.html` | Broker profile | 67 | 137 | ✗ → ✓ | FAQPage | 591 | 0 → 10 | ✓ | ✓ |
| `/brokers/etoro.html` | Broker profile | 61 | 139 | ✗ → ✓ | FAQPage | 523 | 0 → 10 | ✓ | ✓ |
| `/brokers/freedom24.html` | Broker profile | 65 | 149 | ✗ → ✓ | FAQPage | 438 | 0 → 10 | ✓ | ✓ |
| `/brokers/interactive-brokers.html` | Broker profile | 75 | 141 | ✗ → ✓ | FAQPage | 565 | 0 → 10 | ✓ | ✓ |
| `/brokers/lightyear.html` | Broker profile | 65 | 122 | ✗ → ✓ | FAQPage | 462 | 0 → 10 | ✓ | ✓ |
| `/brokers/revolut.html` | Broker profile | 71 | 153 | ✗ → ✓ | BreadcrumbList;FAQPage | 1317 | 0 → 11 | ✓ | ✓ |
| `/brokers/scalable-capital.html` | Broker profile | 72 | 140 | ✗ → ✓ | BreadcrumbList;FAQPage | 1302 | 0 → 11 | ✓ | ✓ |
| `/brokers/trade-republic.html` | Broker profile | 70 | 148 | ✗ → ✓ | BreadcrumbList;FAQPage | 1285 | 0 → 11 | ✓ | ✓ |
| `/brokers/trading-212.html` | Broker profile | 67 | 157 | ✗ → ✓ | FAQPage | 579 | 0 → 10 | ✓ | ✓ |
| `/brokers/xtb.html` | Broker profile | 59 | 125 | ✗ → ✓ | FAQPage | 480 | 0 → 10 | ✓ | ✓ |
| `/el/ependyseis-gia-arxarious.html` | Greek | 66 | 175 | ✓ → ✓ | BlogPosting;BreadcrumbList | 3017 | 4 → 4 | ✓ |  |
| `/el/` | Greek | 57 | 153 | ✓ → ✓ | CollectionPage;BreadcrumbList | 244 | 4 → 4 | ✓ |  |
| `/el/ti-einai-etf.html` | Greek | 65 | 158 | ✓ → ✓ | BlogPosting;BreadcrumbList | 3072 | 4 → 4 | ✓ |  |
| `/el/ti-einai-sp-500.html` | Greek | 58 | 157 | ✓ → ✓ | BlogPosting;BreadcrumbList | 2200 | 4 → 4 | ✓ |  |
| `/degiro.html` | Legacy duplicate | 67 | 137 | ✗ → ✗ | FAQPage | 564 | 0 → 0 | ✗ |  |
| `/etoro.html` | Legacy duplicate | 61 | 139 | ✗ → ✗ | FAQPage | 496 | 0 → 0 | ✗ |  |
| `/freedom24.html` | Legacy duplicate | 65 | 149 | ✗ → ✗ | FAQPage | 411 | 0 → 0 | ✗ |  |
| `/interactive-brokers.html` | Legacy duplicate | 75 | 141 | ✗ → ✗ | FAQPage | 539 | 0 → 0 | ✗ |  |
| `/lightyear.html` | Legacy duplicate | 65 | 122 | ✗ → ✗ | FAQPage | 435 | 0 → 0 | ✗ |  |
| `/revolut.html` | Legacy duplicate | 71 | 131 | ✗ → ✗ | FAQPage | 509 | 0 → 0 | ✗ |  |
| `/scalable-capital.html` | Legacy duplicate | 72 | 142 | ✗ → ✗ | FAQPage | 508 | 0 → 0 | ✗ |  |
| `/trade-republic.html` | Legacy duplicate | 70 | 142 | ✗ → ✗ | FAQPage | 500 | 0 → 0 | ✗ |  |
| `/trading-212.html` | Legacy duplicate | 67 | 157 | ✗ → ✗ | FAQPage | 553 | 0 → 0 | ✗ |  |
| `/xtb.html` | Legacy duplicate | 59 | 125 | ✗ → ✗ | FAQPage | 453 | 0 → 0 | ✗ |  |

---

## B. Implemented changes

### B1. Priority pages

| Page | What changed | Why | Search / user intent served |
|---|---|---|---|
| `/blog-how-to-evaluate-etf.html` | Added an "on this page" jump list, "where to find each number" (factsheet, KID, ISIN), a world vs all-world comparison, red flags (leveraged/inverse, thematic, tiny/new funds, wide spreads), and a tick-off checklist (plain checkboxes, no JS). Corrected the ETF Evaluator CTA and made it measurable. Added sources (iShares, MSCI, EUR-Lex PRIIPs and UCITS), Open Graph, one FAQ with matching schema, and a new review date | The page was already strong. The gaps were practical: where to find the data, how to compare look-alike funds, and what to avoid. The tool claim was not supported by the product pages | "how to evaluate an ETF", "how to compare ETFs", "what to look for in an ETF" (informational to practical) |
| `/blog-what-is-index-fund.html` | Rewritten:<br>• direct definition<br>• how index funds work (weighting, replication)<br>• index fund vs ETF table<br>• vs active funds (SPIVA)<br>• real costs with a labelled hypothetical fee example<br>• limits of diversification<br>• risks<br>• UCITS, KID, domicile and income for EU investors<br>• step-by-step next actions, 6 FAQs, sources<br>• tracked CTA to Historical Data and the DCA Simulator<br>Also new title and description, a neutral H1, Article, Breadcrumb and FAQ schema, and Open Graph | The page was thin and did not answer the follow-up questions beginners search next (vs ETF, cost, safety, Europe) | "what is an index fund", "index fund vs ETF", "are index funds safe", "index funds Europe" |
| `/brokers/trade-republic.html` | At-a-glance box, savings plan vs one-off cost example (€1 on €50 = 2%), currency conversion, country availability, EU deposit and investor protection, alternatives with links, pre-account checklist, 5 FAQs with matching schema, Breadcrumb, Open Graph, intent-matched tracked CTA. "Fees last verified" is now shown separately from "Page updated" | Shift the page from a navigational brand query to the comparison and decision-making intent the brief asked for | "Trade Republic fees", "Trade Republic savings plan", "Trade Republic vs Scalable Capital" |
| `/brokers/scalable-capital.html` | Same template, plus FREE vs PRIME+ logic (when a subscription pays for itself), a note that prices change, and Greece availability not confirmed | Same | "Scalable Capital PRIME+ worth it", "Scalable Capital Greece", "Scalable vs Trade Republic" |
| `/brokers/revolut.html` | Same template, plus plans and free-trade allowance, a worked minimum-fee example (€1 minimum = 1% of a €100 trade), FX on USD assets, and recurring-investing caveats | Same | "Revolut investing fees", "Revolut free trades", "Revolut for ETFs" |

### B2. Supporting pages

| Page | What changed | Why |
|---|---|---|
| `/broker-comparison.html` | Pre-rendered broker cards (byte-identical to the JS output). New static "key fees and features" table for all 10 brokers, linking each profile; JS re-renders it from `brokers[]`. "How to read this comparison", a methodology note, a visible FAQ matching the existing schema, a clearer H1 and description, Open Graph, and `data-sf-cta` on the existing CTAs | Comparison content is now in the HTML response, profiles are reachable without JS, and the schema matches the visible content |
| `/blog.html` | "Start here" block with four ordered learning paths (Start Investing, Understand ETFs, Choose a Broker, Build Investing Habits). Index fund card retitled | Turns a flat 51-card grid into a hub and links the broker profiles from the blog |
| 37 older articles (listed in the commit) | One "Read next" box: path name plus three hand-picked next reads. Article text unchanged | Every article now leads to a next useful resource |
| 7 other broker profiles | "Compare with other brokers" now links every profile plus the broker-choice guide | Fixes orphaned profiles |
| `/about.html` | "How we write our guides": sources, review dates, broker data policy, no recommendations, how the product and planned paid tier are presented, corrections contact (the existing `info@steadfolio.eu`) | Transparency, using only practices visible on the site |
| `/` | Organization logo now points to an existing file | Valid structured data |
| 64 pages | Self-referencing canonical | Consolidates duplicate signals (query strings, UTM variants) |
| 5 articles | Corrected FAQPage schema | Structured data must match visible content |
| `sitemap.xml` | 6 missing articles added; lastmod updated for 6 substantively changed pages | Discovery |
| `llms.txt` | 14 missing public pages added (Greek section untouched) | Complete site guide for AI crawlers |
| 70 English pages | `index.html` hrefs changed to `/` | Removes a redirect hop on every home and nav link |
| 2 pages | Overflowing tables wrapped in a scroll container | Mobile usability |

**Expected benefit (no rankings promised):**

- Broker profiles and comparison data become discoverable and indexable without relying on JS rendering.
- The priority pages answer more of the questions searchers actually ask, which may improve CTR and engagement on queries that already earn impressions.
- Visitors get clear next steps, so more of them reach a second page or a relevant tool.
- New CTAs are measurable per page (`cta_id`).

### B3. Untouched by design

- `/el/*`: no change at all.
- The English pages paired with the Greek guides (`blog-what-is-an-etf.html`, `blog-what-is-the-sp-500.html`, `blog-how-to-start-investing.html`) got only the mechanical home-link change.
- All tracking IDs and scripts: `js/` is unchanged. The only addition is `cta-tracking.js` on 6 pages.
- `vercel.json` and `robots.txt` are unchanged.
- No URL changed.

---

## C. Remaining opportunities (prioritised backlog)

**P1: accuracy and duplicates**

1. **Re-verify all broker figures** against official pages and update `LAST_VERIFIED` in `broker-comparison.html` and each profile's "Fees last verified" date. Start with Scalable Capital and Revolut (see A2 #4).
2. **Legacy root broker duplicates** (A2 #8). Proposed change, which needs your approval:
   ```json
   { "source": "/trade-republic.html", "destination": "/brokers/trade-republic.html", "permanent": true }
   ```
   Add one entry like this per broker to `vercel.json` `redirects`, then delete the ten root files. A lower-impact alternative is a `rel="canonical"` on each root file pointing to its `/brokers/` version.
3. **Real author attribution:** name the founder or authors on About and article bylines, with `Person` schema. Only use true, verifiable details.

**P2: content and measurement**

4. **GSC-driven titles and descriptions.** Export per-page queries for the 57 URLs with zero clicks, then rewrite titles only where the query intent is clearly different from the current title.
5. **Upgrade the seven remaining broker profiles** to the new template (after step 1).
6. **Upgrade thin articles,** starting with the "Understand ETFs" and "Start Investing" paths: `what-is-diversification`, `what-is-asset-allocation`, `what-are-bonds`, `compound-interest-explained`, `beginner-investing-mistakes`. Add sources, a review date, a FAQ and an intent-matched tracked CTA.
7. **GA4 setup:**
   - register `cta_id`, `page_language` and `link_url` as event-scoped custom dimensions,
   - mark `cta_click` as a key event,
   - check cross-domain measurement to `app.steadfolio.eu` so sign-ups can be attributed to landing pages.
8. **Article and Breadcrumb schema** plus visible "last reviewed" dates on the remaining articles. Add them only when a page has genuinely been reviewed.

**P3: polish**

9. Open Graph and Twitter tags site-wide, with a dedicated 1200×630 share image.
10. Use "SteadFolio" consistently on the 39 remaining pages.
11. Shorten the homepage meta description; more descriptive titles for About, Blog, FAQ and Pricing.
12. Fix heading skips on `/cookie-policy.html` and `/journey.html`.
13. Decide whether Clarity should run on `/brokers/*` (A2 #20).
14. Optional tooling: a small script that checks the comparison page's static HTML still matches `brokers[]`, run before deploys.
15. Greek cluster: a Greek broker-choice guide would complete the Greek "Choose a Broker" path (business and editorial decision).

**Needs human confirmation (TODO)**

- [ ] Author or founder name, role and any relevant (real) credentials, for About, bylines and schema.
- [ ] Current broker fees, plans and country availability, especially Scalable Capital and Revolut.
- [ ] Whether to redirect and remove the 10 legacy root broker files.
- [ ] Whether `steadfolio-icon-1080.png` exists anywhere. If so, add it to the repo and use it as the Organization logo.
- [ ] That the ETF Evaluator is still included in the free plan (taken from the Greek guide reviewed on 2026-10-06).

---

## D. Verification results

**Executed:**

- No project build, lint or test exists (no package.json, CI or config), so independent checks were run instead.
- HTML validation (`html-validate` 9.7.1, recommended preset, style-only rules off): on all 71 changed HTML files, no file has more findings than on `origin/main`. Remaining findings are pre-existing (mostly a UTF-8 BOM in some files).
- Internal links and anchors: 3,215 internal links checked, including canonicals, hreflang and `/#fragment` targets. **0 broken.**
- JSON-LD: every block on every page parses. FAQPage questions now match visible text on every page that has them.
- Canonical and hreflang: every indexable page has a self-referencing canonical; EN↔EL hreflang is reciprocal (unchanged).
- Tracking: `js/` is identical to `origin/main`. On every page, no script tag, GA ID, Clarity flag or verification tag was removed or changed. The only addition is `cta-tracking.js` on 6 pages.
- Greek pages: `git diff origin/main -- el/` is empty. The 3 paired English pages differ only in home-link hrefs.
- Broker comparison behaviour (Playwright):
  - static cards and summary match the JS-rendered markup exactly,
  - filters dim the expected cards,
  - selecting brokers opens the compare panel,
  - no JS errors.
- Layout: all 85 pages rendered at 375px and 1280px. No horizontal page overflow after this branch (2 pre-existing cases fixed) and no console errors. The changed priority pages were also reviewed visually.

**Not performed (blocked or out of scope):**

- Live-site checks: redirects, status codes, response headers.
- Google Rich Results Test, Search Console URL Inspection, PageSpeed or Lighthouse field data.
- Official broker fee verification.
- Real-device testing.

**Outstanding risks:**

- Broker figures may be stale (A2 #4).
- Legacy duplicates remain (A2 #8).
- The comparison page's static table depends on staying in sync with `brokers[]` for no-JS crawlers. JS always re-renders it from the data for users and rendering crawlers.
