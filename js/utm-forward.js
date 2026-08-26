/**
 * Preserves UTM attribution parameters when a visitor moves from
 * steadfolio.eu to app.steadfolio.eu via any CTA/link.
 *
 * Only forwards utm_source, utm_medium, utm_campaign, utm_content, utm_term
 * when present on the current page's URL. Links are left untouched when no
 * UTM parameters are present.
 */
(function () {
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];

  function buildTargetHref(anchor) {
    var url;
    try {
      url = new URL(anchor.href, window.location.href);
    } catch (e) {
      return null;
    }
    if (url.hostname !== 'app.steadfolio.eu') return null;

    var incoming = new URLSearchParams(window.location.search);
    var changed = false;
    UTM_KEYS.forEach(function (key) {
      var value = incoming.get(key);
      if (value && !url.searchParams.has(key)) {
        url.searchParams.set(key, value);
        changed = true;
      }
    });
    return changed ? url.toString() : null;
  }

  function rewriteLink(anchor) {
    var newHref = buildTargetHref(anchor);
    if (newHref) anchor.setAttribute('href', newHref);
  }

  function rewriteAllLinks() {
    var anchors = document.querySelectorAll('a[href]');
    for (var i = 0; i < anchors.length; i++) {
      rewriteLink(anchors[i]);
    }
  }

  function handleClick(event) {
    var anchor = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (anchor) rewriteLink(anchor);
  }

  // Rewrite links already in the DOM, and any added dynamically afterwards
  // (e.g. links injected by on-page interactions) right before navigation.
  document.addEventListener('click', handleClick, true);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', rewriteAllLinks);
  } else {
    rewriteAllLinks();
  }
})();
