/* Site-wide behaviour. Plain browser JavaScript, no framework. */

(function () {
  "use strict";

  /* Fade sections in as they scroll into view.
     Anything marked .reveal starts hidden in CSS, so if this script fails to
     run we must still show it — hence the immediate fallback below. */
  var revealables = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("in"); });
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          observer.unobserve(entry.target);   // reveal once, not on every scroll
        }
      });
    }, { rootMargin: "0px 0px -80px 0px", threshold: 0.08 });

    revealables.forEach(function (el) { observer.observe(el); });
  }
})();


/* Move the navigation underline to whichever section you are reading.
   Homepage only: its sections mirror the standalone pages, and each one
   carries data-nav with the matching nav href. */
(function () {
  "use strict";

  var sections = document.querySelectorAll("[data-nav]");
  var links = document.querySelectorAll(".site-nav a");
  if (!sections.length || !links.length) return;

  var byHref = {};
  links.forEach(function (a) {
    byHref[a.getAttribute("href")] = a;
  });

  function highlight(href) {
    links.forEach(function (a) {
      var on = a === byHref[href];
      a.classList.toggle("is-current", on);
      if (on) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  if (!("IntersectionObserver" in window)) return;

  // Track how much of each section is on screen and light up the largest.
  // Picking "the first one intersecting" makes the underline flicker between
  // two neighbours while a long section scrolls past.
  var visible = {};

  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var href = entry.target.getAttribute("data-nav");
      visible[href] = entry.isIntersecting ? entry.intersectionRatio : 0;
    });

    var best = null;
    var bestRatio = 0;
    Object.keys(visible).forEach(function (href) {
      if (visible[href] > bestRatio) {
        bestRatio = visible[href];
        best = href;
      }
    });

    if (best) highlight(best);
  }, {
    // Discount the sticky header, so a section counts as "read" only once it
    // is genuinely in view rather than tucked behind the bar.
    rootMargin: "-72px 0px -35% 0px",
    threshold: [0, 0.15, 0.35, 0.6, 0.9],
  });

  sections.forEach(function (section) { spy.observe(section); });
})();
