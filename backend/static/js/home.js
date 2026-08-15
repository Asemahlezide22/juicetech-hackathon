/* Homepage: live station card, fed by the Python API.

   Polls every 10 seconds so the numbers visibly move when somebody rents or
   returns a power bank. If the API is unreachable the card says so rather
   than showing stale figures dressed up as live ones. */

(function () {
  "use strict";

  var card = document.getElementById("live-card");
  if (!card) return;

  var stationId = card.dataset.station;

  var els = {
    status: document.getElementById("live-status"),
    id: document.getElementById("live-id"),
    venue: document.getElementById("live-venue"),
    available: document.getElementById("live-available"),
    rented: document.getElementById("live-rented"),
    foot: document.getElementById("live-foot"),
  };

  /** Count from the current value to the new one, so numbers feel alive. */
  function countTo(el, target) {
    var from = parseInt(el.textContent, 10);
    if (isNaN(from)) from = 0;

    if (from === target) {
      // Still write it — the cell may be showing the "—" placeholder, and a
      // real value of 0 would otherwise never replace it.
      el.textContent = target;
      return;
    }

    var steps = Math.min(Math.abs(target - from), 12);
    var step = (target - from) / steps;
    var current = from;
    var i = 0;

    var timer = setInterval(function () {
      i += 1;
      current += step;
      el.textContent = i >= steps ? target : Math.round(current);
      if (i >= steps) clearInterval(timer);
    }, 45);
  }

  function paint(station) {
    els.id.textContent = station.id;
    els.venue.textContent = station.venue;
    countTo(els.available, station.available);
    countTo(els.rented, station.rented);

    els.status.textContent = station.online ? "Station online" : "Station offline";
    els.status.style.color = station.online ? "" : "var(--dim)";

    els.foot.textContent = "Live from the station network";
  }

  function refresh() {
    fetch("/api/stations/" + encodeURIComponent(stationId))
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(paint)
      .catch(function () {
        els.foot.textContent = "Live data unavailable";
      });
  }

  refresh();
  setInterval(refresh, 10000);
})();
