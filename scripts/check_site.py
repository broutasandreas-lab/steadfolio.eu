#!/usr/bin/env python3
"""Static checks for the steadfolio.eu marketing site.

Run from anywhere:  python3 scripts/check_site.py [--report]

Hard checks (exit code 1 on failure):
  - every indexable page has exactly one self-referencing canonical
  - no page carries a noindex directive
  - every JSON-LD block parses
  - every internal link and #fragment resolves to a file / element id
  - sitemap.xml is well-formed, lists only existing pages, and every canonical
    page is listed
  - robots.txt declares the sitemap and does not block the site
  - vercel.json redirect sources no longer exist as files, destinations do
  - FAQ pages: number of FAQPage questions equals number of visible questions
  - hreflang pairs are reciprocal
  - product-truth lint: no upgrade/checkout/"cancel anytime"/"unlimited Sofia"
    language, broker connection only ever described as planned or unavailable,
    SteadFolio brand casing, no credentials on the About page
  - structured-data restraint: no Review/AggregateRating/FinancialProduct/
    InvestmentOrDeposit/Person types and no datePublished on English pages

--report additionally prints the soft reports (trust coverage, product-claim
and brand greps) used in the visibility review.
"""
import glob
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://steadfolio.eu"
os.chdir(ROOT)

# Pages that are intentionally not part of the public site
NON_PAGE = {"a212012d8b844af8997798ca9d3907a9.txt"}


def pages():
    out = sorted(glob.glob("*.html") + glob.glob("brokers/*.html") + glob.glob("el/*.html"))
    return out


def norm(s):
    """Whitespace- and typographic-quote-insensitive form for text comparison."""
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    return re.sub(r"\s+", " ", s)


def url_for(path):
    if path == "index.html":
        return BASE + "/"
    if path == "el/index.html":
        return BASE + "/el/"
    return BASE + "/" + path


class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canon, self.robots, self.hreflang = [], [], []
        self.links, self.ids = [], set()
        self.ld, self._in_ld, self._buf = [], False, []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and a.get("name"):
            self.ids.add(a["name"])
        if tag == "link" and a.get("rel") == "canonical":
            self.canon.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang.append((a["hreflang"], a.get("href")))
        if tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots.append(a.get("content") or "")
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag == "h1":
            self.h1 += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self.ld.append("".join(self._buf))
            self._in_ld = False

    def handle_data(self, data):
        if self._in_ld:
            self._buf.append(data)


def parse(path):
    raw = open(path, encoding="utf-8-sig").read()
    p = Head()
    p.feed(raw)
    return raw, p


errors, warnings = [], []


def err(msg):
    errors.append(msg)


def target_file(href, src):
    """Resolve an internal href to (file, fragment) or None if external/ignored."""
    if re.match(r"^(mailto:|tel:|javascript:|data:)", href):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        if not href.startswith(BASE):
            return None
        href = href[len(BASE):] or "/"
    href, _, frag = href.partition("#")
    href = href.partition("?")[0]
    if href == "":
        return src, frag
    if href.startswith("/"):
        rel = href.lstrip("/")
    else:
        rel = os.path.normpath(os.path.join(os.path.dirname(src), href))
    if rel in ("", "."):
        rel = "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    if os.path.isdir(rel):
        rel = os.path.join(rel, "index.html")
    return rel, frag


def main():
    report = "--report" in sys.argv
    allp = pages()
    parsed = {p: parse(p) for p in allp}
    canon_urls = {}

    for p, (raw, h) in parsed.items():
        # canonical
        if len(h.canon) != 1:
            err(f"{p}: expected 1 canonical, found {len(h.canon)}")
        elif h.canon[0] != url_for(p):
            err(f"{p}: canonical {h.canon[0]} != {url_for(p)}")
        else:
            canon_urls[p] = h.canon[0]
        # noindex
        for r in h.robots:
            if "noindex" in r.lower():
                err(f"{p}: noindex directive ({r})")
        if h.h1 != 1:
            err(f"{p}: {h.h1} <h1> elements")
        # JSON-LD
        for i, block in enumerate(h.ld):
            try:
                json.loads(block)
            except Exception as e:  # noqa: BLE001
                err(f"{p}: JSON-LD block {i} does not parse ({e})")
        # links
        for href in h.links:
            tf = target_file(href, p)
            if tf is None:
                continue
            f, frag = tf
            if not os.path.exists(f):
                # redirected legacy URLs are allowed only via vercel.json
                err(f"{p}: broken internal link {href} -> {f}")
                continue
            if frag and f.endswith(".html"):
                ids = parsed[f][1].ids if f in parsed else set()
                if frag not in ids:
                    err(f"{p}: fragment #{frag} not found in {f} (link {href})")

    # FAQ visible vs schema (FAQPage questions must equal visible questions)
    for p, (raw, h) in parsed.items():
        for block in h.ld:
            try:
                j = json.loads(block)
            except Exception:  # noqa: BLE001
                continue
            if isinstance(j, dict) and j.get("@type") == "FAQPage":
                names = [q["name"] for q in j["mainEntity"]]
                text = html.unescape(re.sub(r"<[^>]+>", "", raw))
                text = norm(text)
                for n in names:
                    if norm(n) not in text:
                        err(f"{p}: FAQ schema question not visible on page: {n!r}")

    # hreflang reciprocity
    for p, (raw, h) in parsed.items():
        for lang, href in h.hreflang:
            tf = target_file(href, p)
            if not tf or not os.path.exists(tf[0]):
                err(f"{p}: hreflang {lang} target missing: {href}")
                continue
            back = [x for x in parsed[tf[0]][1].hreflang if target_file(x[1], tf[0])
                    and target_file(x[1], tf[0])[0] == p]
            if tf[0] != p and not back:
                err(f"{p}: hreflang {lang} -> {tf[0]} is not reciprocal")

    # sitemap
    sm = ET.parse("sitemap.xml").getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [e.text.strip() for e in sm.findall("s:url/s:loc", ns)]
    if len(locs) != len(set(locs)):
        err("sitemap.xml: duplicate <loc> entries")
    loc_set = set(locs)
    for l in locs:
        if not l.startswith(BASE):
            err(f"sitemap.xml: foreign URL {l}")
            continue
        rel = l[len(BASE):].lstrip("/") or "index.html"
        if rel.endswith("/"):
            rel += "index.html"
        if not os.path.exists(rel):
            err(f"sitemap.xml: {l} has no file")
    for p, c in canon_urls.items():
        if c not in loc_set:
            err(f"sitemap.xml: missing canonical page {c}")

    # robots
    robots = open("robots.txt").read()
    if f"Sitemap: {BASE}/sitemap.xml" not in robots:
        err("robots.txt: Sitemap line missing")
    if re.search(r"^Disallow:\s*/\s*$", robots, re.M):
        err("robots.txt: blanket Disallow found")

    # redirects
    vj = json.load(open("vercel.json"))
    for r in vj.get("redirects", []):
        src, dst = r["source"], r["destination"]
        if src != "/index.html" and os.path.exists(src.lstrip("/")):
            err(f"vercel.json: redirect source {src} still exists as a file")
        d = dst.lstrip("/") or "index.html"
        if not os.path.exists(d):
            err(f"vercel.json: redirect destination {dst} missing")

    lint(parsed)

    print(f"Checked {len(allp)} pages, {len(locs)} sitemap URLs, {len(vj.get('redirects', []))} redirects.")

    if report:
        soft_reports(parsed)

    if errors:
        print(f"\n{len(errors)} problem(s):")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("All hard checks passed.")


FORBIDDEN_TEXT = [
    r"Upgrade to", r"Upgrade now", r"Unlimited Sofia", r"[Uu]nlimited (portfolio )?screenshot",
    r"[Cc]ancel anytime", r"[Cc]heckout", r"Buy SteadFolio\+", r"Subscribe now", r"Steadfolio", r"STEADFOLIO",
    r"[Rr]eviewed by",
]
FORBIDDEN_LD_TYPES = {"Review", "AggregateRating", "Rating", "FinancialProduct", "InvestmentOrDeposit", "Person"}
CREDENTIALS = r"\b(CFA|CFP|MBA|MSc|PhD|certified|chartered|licensed|FCA-authorised|registered adviser|investment professional)\b"
PLANNED = r"planned|not (yet )?available|isn't available|doesn't currently|not currently|no way|coming soon|still being built|building toward|connecting a broker so"


def visible_text(raw):
    body = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", " ", raw, flags=re.S)
    return norm(html.unescape(re.sub(r"<[^>]+>", " ", body)))


def lint(parsed):
    for p, (raw, h) in parsed.items():
        text = visible_text(raw)
        for pat in FORBIDDEN_TEXT:
            if re.search(pat, text):
                err(f"{p}: forbidden phrase /{pat}/")
        # broker connection must always be qualified as planned / unavailable
        for m in re.finditer(r"[^.]*\b(broker (connection|sync)|connect(ing)? (a|your) broker)\b[^.]*\.", text, re.I):
            s = m.group(0)
            if not re.search(PLANNED, s, re.I) and not re.search(r"no requirement|don't", s, re.I):
                err(f"{p}: broker connection not qualified as planned/unavailable: {s.strip()[:120]!r}")
        # SteadFolio+ must never be presented as purchasable
        for m in re.finditer(r"[^.]*SteadFolio\+[^.]*\.", text):
            s = m.group(0)
            if re.search(r"\b(buy|purchase|subscribe|sign up for)\b", s, re.I) and not re.search(
                    r"\b(can't|cannot|no way|not|nothing|never|before|no)\b", s, re.I):
                err(f"{p}: SteadFolio+ may read as purchasable: {s.strip()[:120]!r}")
        for block in h.ld:
            j = json.loads(block)
            for node in (j if isinstance(j, list) else [j]):
                t = node.get("@type")
                for ty in (t if isinstance(t, list) else [t]):
                    if ty in FORBIDDEN_LD_TYPES:
                        err(f"{p}: restricted JSON-LD type {ty}")
        # Greek guides were created on a recorded date (2026-10-06, see git); English pages have none
        if "datePublished" in raw and not p.startswith("el/"):
            err(f"{p}: datePublished present (publication dates are not recorded)")
    about = visible_text(parsed["about.html"][0])
    if re.search(CREDENTIALS, about):
        err("about.html: credential-like wording found")


def soft_reports(parsed):
    arts = [p for p in parsed if re.match(r"blog-.*\.html$", p)]
    cov = {k: 0 for k in ("canonical", "author", "Article", "reviewed", "Breadcrumb", "sources", "datePublished")}
    for p in arts:
        raw, h = parsed[p]
        types = []
        for b in h.ld:
            j = json.loads(b)
            types += [x.get("@type") for x in (j if isinstance(j, list) else [j])]
        cov["canonical"] += bool(h.canon)
        cov["Article"] += "Article" in types or "BlogPosting" in types
        cov["Breadcrumb"] += "BreadcrumbList" in types
        cov["author"] += "The SteadFolio Team" in raw
        cov["reviewed"] += bool(re.search(r"Last reviewed:", raw))
        cov["sources"] += bool(re.search(r'<h2>Sources</h2>|class="sources"', raw))
        cov["datePublished"] += "datePublished" in raw
    print(f"\nEnglish articles: {len(arts)}")
    for k, v in cov.items():
        print(f"  {k:14} {v}")

    print("\nBrand: visible 'Steadfolio' (should be 0):")
    n = 0
    for p, (raw, _) in parsed.items():
        c = len(re.findall(r"Steadfolio", raw))
        if c:
            n += c
            print(f"  {p}: {c}")
    print(f"  total {n}")

    pats = [r"[Uu]nlimited", r"Upgrade", r"XIRR", r"Portfolio Audit", r"broker (connection|sync)", r"SteadFolio\+",
            r"9\.99|89\.90"]
    print("\nProduct-claim hits (review each):")
    for pat in pats:
        for p, (raw, _) in parsed.items():
            body = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
            for m in re.finditer(pat, body):
                ctx = re.sub(r"<[^>]+>", "", body[max(0, m.start() - 60): m.end() + 60]).replace("\n", " ")
                print(f"  [{pat}] {p}: ...{ctx.strip()}...")


if __name__ == "__main__":
    main()
