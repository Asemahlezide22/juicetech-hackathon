/* Site-wide behaviour. Plain browser JavaScript, no framework. */

(function () {
  "use strict";

  /* Fade sections in as they scroll into view.
     Anything marked .reveal starts hidden in CSS, so if this script fails to
     run we must still show it — hence the immediate fallback below. */
  var revealables = document.querySelectorAll(".reveal");

  if (!("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("in"); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("in");
        observer.unobserve(entry.target);   // reveal once, not on every scroll
      }
    });
  }, { rootMargin: "0px 0px -80px 0px", threshold: 0.08 });

  revealables.forEach(function (el) { observer.observe(el); });
})();
