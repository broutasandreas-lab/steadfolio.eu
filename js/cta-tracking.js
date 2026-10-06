/**
 * CTA click measurement (marketing site).
 *
 * Sends one GA4 "cta_click" event when a visitor clicks a link marked with
 * data-sf-cta="<id>". Only opted-in links are tracked, so adding this
 * script to a page has no effect on any other link.
 *
 * Consent: events are only queued when the shared consent cookie
 * (steadfolio_consent_v1, set by cookie-consent.js) is "accepted", so
 * nothing is queued for visitors who reject or have not chosen yet.
 *
 * Event parameters (register as event-scoped custom dimensions in GA4):
 *   cta_id        - the data-sf-cta value, e.g. "el_etf_inline"
 *   page_language - <html lang>, e.g. "el"
 *   link_url      - destination URL
 */
(function () {
  function hasAnalyticsConsent() {
    return /(?:^|; )steadfolio_consent_v1=accepted(?:;|$)/.test(document.cookie);
  }

  function handleClick(event) {
    var anchor = event.target && event.target.closest ? event.target.closest('a[data-sf-cta]') : null;
    if (!anchor || typeof window.gtag !== 'function' || !hasAnalyticsConsent()) return;
    window.gtag('event', 'cta_click', {
      cta_id: anchor.getAttribute('data-sf-cta'),
      page_language: (document.documentElement.lang || '').toLowerCase(),
      link_url: anchor.href,
      transport_type: 'beacon'
    });
  }

  document.addEventListener('click', handleClick);
})();
