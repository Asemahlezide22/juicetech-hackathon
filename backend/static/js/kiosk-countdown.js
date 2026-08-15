/* Scan to Pay countdown.

   Purely presentational: the demo never actually expires a rental, so a
   judge who leaves the screen open mid-pitch is not locked out. When it
   reaches zero it says so and stops. */

(function () {
  "use strict";

  var el = document.getElementById("countdown");
  if (!el) return;

  var minutes = parseInt(el.dataset.minutes, 10);
  if (isNaN(minutes)) minutes = 15;

  var remaining = minutes * 60;

  function paint() {
    var m = Math.floor(remaining / 60);
    var s = remaining % 60;
    el.textContent = m + ":" + (s < 10 ? "0" : "") + s;
  }

  paint();

  var timer = setInterval(function () {
    remaining -= 1;

    if (remaining <= 0) {
      clearInterval(timer);
      el.textContent = "expired";
      var wrap = el.closest(".k-countdown");
      if (wrap) {
        wrap.classList.add("is-expired");
        wrap.insertAdjacentHTML(
          "beforeend",
          " &mdash; you can still use the button below."
        );
      }
      return;
    }

    paint();
  }, 1000);
})();
