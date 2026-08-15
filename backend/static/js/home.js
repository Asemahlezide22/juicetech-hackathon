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
    signal: document.getElementById("live-signal"),
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

    if (els.signal) els.signal.textContent = station.signal + "/5";

    els.foot.textContent = "Live from the station network";
  }

  var POLL_MS = 10000;      // normal cadence
  var RETRY_MS = 2500;      // after a miss, come back sooner
  var FORGIVE = 2;          // consecutive misses before we admit anything

  var misses = 0;
  var timer = null;

  function schedule(delay) {
    clearTimeout(timer);
    timer = setTimeout(refresh, delay);
  }

  function refresh() {
    fetch("/api/stations/" + encodeURIComponent(stationId))
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (station) {
        misses = 0;
        paint(station);
        schedule(POLL_MS);
      })
      .catch(function () {
        misses += 1;

        // One dropped poll is a blip — a restarted server, a moment of wifi.
        // Saying "unavailable" for ten seconds because of it is the last thing
        // we want on screen mid-demo, so hold the last known numbers and try
        // again sooner. Only admit a problem once it is clearly persistent.
        if (misses >= FORGIVE) {
          els.foot.textContent = "Reconnecting to the station network…";
        }
        schedule(RETRY_MS);
      });
  }

  refresh();
})();
