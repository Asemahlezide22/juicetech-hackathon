/* Site-wide behaviour. Plain browser JavaScript, no framework. */

(function () {
  "use strict";

  /* Fade sections in as they scroll into view.

     Sections are visible unless the inline script in <head> armed the
     effect, so there is nothing to rescue when this file fails to load.
     What this does add is cancelling that script's 2.5s failsafe — but only
     once a reveal has actually happened, which is the only proof that the
     observer is really firing. */
  var revealables = document.querySelectorAll(".reveal");
  if (!revealables.length) return;

  if (!("IntersectionObserver" in window)) {
    document.documentElement.classList.remove("reveal-armed");
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;

      if (window.__jtDisarm) {
        clearTimeout(window.__jtDisarm);
        window.__jtDisarm = null;
      }

      entry.target.classList.add("in");
      observer.unobserve(entry.target);   // reveal once, not on every scroll
    });
  }, { rootMargin: "0px 0px -80px 0px", threshold: 0.08 });

  revealables.forEach(function (el) { observer.observe(el); });
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

/* ---------- Colour mode ----------

   The theme itself is applied by an inline script in <head>, before the page
   paints. This only wires up the button and remembers the choice.

   Three states, not two: "dark", "light", and no stored preference at all,
   which follows the device. Once someone presses the button they have made a
   choice, and it outranks the device from then on. */
(function () {
  var toggle = document.querySelector(".theme-toggle");
  if (!toggle) return;

  var root = document.documentElement;

  function devicePrefersDark() {
    return window.matchMedia
      && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function currentlyDark() {
    var chosen = root.getAttribute("data-theme");
    if (chosen === "dark") return true;
    if (chosen === "light") return false;
    return devicePrefersDark();
  }

  function describe() {
    var dark = currentlyDark();
    // The label says what the button will DO, which is what a screen reader
    // user needs; aria-pressed says what the page currently IS.
    toggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    toggle.setAttribute("aria-pressed", dark ? "true" : "false");
  }

  toggle.addEventListener("click", function () {
    var next = currentlyDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem("jt-theme", next);
    } catch (e) {
      /* Refused storage only costs persistence — the page still switches. */
    }
    describe();
  });

  // Someone who has never pressed the button keeps following their device,
  // even if they change it while the page is open.
  if (window.matchMedia) {
    var watch = window.matchMedia("(prefers-color-scheme: dark)");
    var onChange = function () {
      if (!root.getAttribute("data-theme")) describe();
    };
    if (watch.addEventListener) watch.addEventListener("change", onChange);
    else if (watch.addListener) watch.addListener(onChange);
  }

  describe();
})();

/* ---------- Mobile menu ----------

   The nav is a plain visible list until this runs. Only once we know the
   script is alive do we collapse it behind a button — otherwise a phone that
   fails to load site.js would show a menu button that does nothing and no way
   to reach the rest of the site. */
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;

  // Matches the CSS breakpoint. If these two ever disagree, the nav hides on
  // a screen with no button to bring it back.
  var mobile = window.matchMedia("(max-width: 860px)");

  function open() {
    nav.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Close menu");
  }

  function close() {
    nav.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
  }

  function isOpen() {
    return toggle.getAttribute("aria-expanded") === "true";
  }

  function apply() {
    if (mobile.matches) {
      close();
    } else {
      // On a wide screen the nav is a row and must never stay hidden — a
      // phone rotated to landscape, or a window dragged wider, would
      // otherwise lose its navigation entirely.
      nav.hidden = false;
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }
  }

  toggle.addEventListener("click", function () {
    isOpen() ? close() : open();
  });

  // A tap on a link navigates; closing first stops the menu flashing over
  // the top of the new page on same-page anchors.
  nav.addEventListener("click", function (event) {
    if (event.target.closest("a") && mobile.matches) close();
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && isOpen()) {
      close();
      toggle.focus();     // don't strand focus inside a menu that just closed
    }
  });

  document.addEventListener("click", function (event) {
    if (!isOpen() || !mobile.matches) return;
    if (!event.target.closest(".site-header")) close();
  });

  if (mobile.addEventListener) mobile.addEventListener("change", apply);
  else if (mobile.addListener) mobile.addListener(apply);

  /* And again on resize, because the matchMedia change event is not
     dependable everywhere — under test it did not fire at all. Missing it
     leaves hidden="" on a nav that is visibly a row: it looks perfectly
     fine, and screen readers skip the site's entire navigation. Cheap
     insurance against a fault nobody would catch by looking at it. */
  var pending;
  window.addEventListener("resize", function () {
    clearTimeout(pending);
    pending = setTimeout(apply, 120);
  });

  apply();
})();
