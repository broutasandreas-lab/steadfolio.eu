/**
 * SteadFolio analytics consent (marketing site).
 *
 * Two-state consent: "accepted" / "rejected" analytics. Advertising
 * consent is never granted from this site. The choice is stored in a
 * cookie shared with app.steadfolio.eu via the .steadfolio.eu domain,
 * per the shared consent contract:
 *
 *   name:   steadfolio_consent_v1
 *   domain: .steadfolio.eu
 *   path:   /
 *   values: "accepted" | "rejected"
 *
 * Google Analytics (gtag.js) and Microsoft Clarity are only fetched
 * after the visitor accepts - nothing is loaded, and no analytics
 * cookie is set, before a choice is made or after a rejection.
 */
(function () {
  var COOKIE_NAME = 'steadfolio_consent_v1';
  var GA_ID = 'G-V3SFS38ZZL';
  var CLARITY_ID = 'y2tjex4mri';
  var hasClarity = document.currentScript && document.currentScript.getAttribute('data-clarity') === '1';

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return match ? decodeURIComponent(match[1]) : null;
  }

  function setCookie(value) {
    var parts = [COOKIE_NAME + '=' + encodeURIComponent(value), 'path=/', 'max-age=' + 60 * 60 * 24 * 365, 'SameSite=Lax'];
    var host = window.location.hostname;
    if (host === 'steadfolio.eu' || host.indexOf('.steadfolio.eu') !== -1) {
      parts.push('domain=.steadfolio.eu');
    }
    if (window.location.protocol === 'https:') {
      parts.push('Secure');
    }
    document.cookie = parts.join('; ');
  }

  function ensureGtagStub() {
    window.dataLayer = window.dataLayer || [];
    if (!window.gtag) {
      window.gtag = function () { window.dataLayer.push(arguments); };
    }
  }

  function ensureClarityStub() {
    if (!window.clarity) {
      window.clarity = function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
    }
  }

  function establishDefaults() {
    ensureGtagStub();
    gtag('consent', 'default', {
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      analytics_storage: 'denied'
    });
    if (hasClarity) ensureClarityStub();
  }

  function loadGaScript() {
    if (document.getElementById('sf-ga-script')) return;
    var s = document.createElement('script');
    s.id = 'sf-ga-script';
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    gtag('js', new Date());
  }

  function loadClarityScript() {
    if (document.getElementById('sf-clarity-script')) return;
    var s = document.createElement('script');
    s.id = 'sf-clarity-script';
    s.async = true;
    s.src = 'https://www.clarity.ms/tag/' + CLARITY_ID;
    var first = document.getElementsByTagName('script')[0];
    first.parentNode.insertBefore(s, first);
  }

  function enableAnalytics() {
    ensureGtagStub();
    gtag('consent', 'update', { analytics_storage: 'granted' });
    gtag('config', GA_ID);
    loadGaScript();
    if (hasClarity) {
      ensureClarityStub();
      loadClarityScript();
      clarity('consent');
    }
  }

  function disableAnalytics() {
    if (window.gtag) {
      gtag('consent', 'update', { analytics_storage: 'denied' });
    }
    if (hasClarity && window.clarity) {
      try { clarity('consent', false); } catch (e) { /* no-op if unsupported */ }
    }
  }

  function applyConsent(value) {
    if (value === 'accepted') {
      enableAnalytics();
    } else if (value === 'rejected') {
      disableAnalytics();
    }
  }

  var COPY = {
    en: {
      message: 'We use optional analytics to understand how SteadFolio is used and improve the experience. Essential functionality works without analytics.',
      accept: 'Accept analytics',
      reject: 'Reject non-essential',
      settings: 'Cookie settings'
    },
    el: {
      message: 'Χρησιμοποιούμε προαιρετικά analytics για να κατανοήσουμε πώς χρησιμοποιείται το SteadFolio και να βελτιώσουμε την εμπειρία. Οι βασικές λειτουργίες λειτουργούν χωρίς analytics.',
      accept: 'Αποδοχή analytics',
      reject: 'Απόρριψη μη απαραίτητων',
      settings: 'Ρυθμίσεις cookies'
    }
  };

  function getLang() {
    var htmlLang = (document.documentElement.lang || '').toLowerCase();
    return htmlLang.indexOf('el') === 0 ? 'el' : 'en';
  }

  var STYLE = '' +
    '#sf-cookie-banner{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;' +
    'max-width:640px;margin:0 auto;background:#0d1620;color:#eef4f1;border:1px solid #1c2b3a;' +
    'border-radius:14px;padding:18px 20px;box-shadow:0 12px 32px rgba(0,0,0,.35);' +
    'font-family:Inter,sans-serif;font-size:14px;line-height:1.5;}' +
    '#sf-cookie-banner p{margin:0 0 14px;}' +
    '#sf-cookie-banner .sf-cc-actions{display:flex;gap:10px;flex-wrap:wrap;}' +
    '#sf-cookie-banner button{flex:1 1 160px;cursor:pointer;border-radius:8px;padding:10px 16px;' +
    'font-family:inherit;font-size:14px;font-weight:600;border:1px solid #1c2b3a;}' +
    '#sf-cc-accept{background:#22c58b;color:#070b10;border-color:#22c58b;}' +
    '#sf-cc-reject{background:transparent;color:#eef4f1;}' +
    '#sf-cc-accept:hover{background:#34d399;}' +
    '#sf-cc-reject:hover{background:#101c28;}' +
    '@media (max-width:480px){#sf-cookie-banner{left:8px;right:8px;bottom:8px;padding:16px;}}';

  function injectStyle() {
    if (document.getElementById('sf-cookie-consent-style')) return;
    var style = document.createElement('style');
    style.id = 'sf-cookie-consent-style';
    style.textContent = STYLE;
    document.head.appendChild(style);
  }

  function removeBanner() {
    var el = document.getElementById('sf-cookie-banner');
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function showBanner() {
    removeBanner();
    injectStyle();
    var copy = COPY[getLang()];
    var banner = document.createElement('div');
    banner.id = 'sf-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', copy.settings);

    var message = document.createElement('p');
    message.textContent = copy.message;

    var actions = document.createElement('div');
    actions.className = 'sf-cc-actions';

    var acceptBtn = document.createElement('button');
    acceptBtn.type = 'button';
    acceptBtn.id = 'sf-cc-accept';
    acceptBtn.textContent = copy.accept;
    acceptBtn.addEventListener('click', function () {
      setCookie('accepted');
      applyConsent('accepted');
      removeBanner();
    });

    var rejectBtn = document.createElement('button');
    rejectBtn.type = 'button';
    rejectBtn.id = 'sf-cc-reject';
    rejectBtn.textContent = copy.reject;
    rejectBtn.addEventListener('click', function () {
      setCookie('rejected');
      applyConsent('rejected');
      removeBanner();
    });

    actions.appendChild(acceptBtn);
    actions.appendChild(rejectBtn);
    banner.appendChild(message);
    banner.appendChild(actions);
    document.body.appendChild(banner);
  }

  function injectSettingsLink() {
    var container = document.querySelector('.footer-links');
    if (!container || document.getElementById('sf-cookie-settings')) return;
    var link = document.createElement('a');
    link.href = '#';
    link.id = 'sf-cookie-settings';
    link.textContent = COPY[getLang()].settings;
    link.addEventListener('click', function (e) {
      e.preventDefault();
      showBanner();
    });
    container.appendChild(link);
  }

  function init() {
    establishDefaults();
    var consent = getCookie(COOKIE_NAME);
    if (consent === 'accepted' || consent === 'rejected') {
      applyConsent(consent);
    } else {
      showBanner();
    }
    injectSettingsLink();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
