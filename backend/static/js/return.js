/* "Find nearest station" — plain browser JavaScript, no framework.
   Talks to the Python API at /api/stations/nearest. */

(function () {
  "use strict";

  var findBtn = document.getElementById("find-btn");
  var suburbBtn = document.getElementById("suburb-btn");
  var suburbSelect = document.getElementById("suburb");
  var onlyFree = document.getElementById("only-free");
  var statusEl = document.getElementById("status");
  var manualEl = document.getElementById("manual");
  var resultsEl = document.getElementById("results");

  // Remembered so the "only free slots" toggle can re-search without asking
  // for the location again.
  var lastPosition = null;

  function setStatus(message, isError) {
    statusEl.textContent = message;
    statusEl.classList.toggle("error", Boolean(isError));
  }

  function showManualPicker() {
    manualEl.hidden = false;
  }

  /** Escape text before putting it in innerHTML. */
  function esc(value) {
    return String(value).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function stationBadge(station) {
    if (!station.online) {
      return '<span class="pill pill-offline">Offline</span>';
    }
    if (station.free_slots <= 0) {
      return '<span class="pill pill-full">Full &mdash; cannot accept returns</span>';
    }
    return '<span class="pill pill-ok">' + station.free_slots + " free slot" +
      (station.free_slots === 1 ? "" : "s") + "</span>";
  }

  function render(stations) {
    resultsEl.innerHTML = "";

    if (!stations.length) {
      resultsEl.innerHTML =
        '<li class="empty">No stations found nearby. Try turning off the ' +
        '&ldquo;free slot&rdquo; filter, or contact support on 073 407 2268.</li>';
      return;
    }

    stations.forEach(function (station, index) {
      var canReturn = station.online && station.free_slots > 0;
      var item = document.createElement("li");

      // Only highlight the top result when it can actually take a bank.
      item.className = "station" + (index === 0 && canReturn ? " is-nearest" : "");

      item.innerHTML =
        '<div class="station-rank">' + (index + 1) + "</div>" +
        '<div class="station-body">' +
          '<p class="station-name">' + esc(station.venue) + "</p>" +
          '<p class="station-address">' + esc(station.address || station.id) + "</p>" +
          '<div class="station-facts">' +
            '<span class="fact distance">' + station.distance_km.toFixed(2) + " km</span>" +
            '<span class="fact">' + station.walking_minutes + " min walk</span>" +
            '<span class="fact"><strong>' + station.available + "</strong>&nbsp;charged</span>" +
            "<span class=\"fact\">" + stationBadge(station) + "</span>" +
          "</div>" +
        "</div>";

      resultsEl.appendChild(item);
    });
  }

  function search(lat, lng) {
    lastPosition = { lat: lat, lng: lng };

    var url = "/api/stations/nearest?lat=" + encodeURIComponent(lat) +
      "&lng=" + encodeURIComponent(lng) + "&limit=10";

    if (onlyFree.checked) {
      url += "&for_return=true";
    }

    setStatus("Finding stations near you…");
    findBtn.disabled = true;

    fetch(url)
      .then(function (response) {
        if (!response.ok) throw new Error("Station lookup failed (" + response.status + ")");
        return response.json();
      })
      .then(function (stations) {
        render(stations);
        if (stations.length) {
          setStatus(
            "Closest: " + stations[0].venue + " — " +
            stations[0].distance_km.toFixed(2) + " km away."
          );
        } else {
          setStatus("No matching stations found.", true);
        }
      })
      .catch(function (error) {
        setStatus(error.message + " Is the Juice Tech API running?", true);
        showManualPicker();
      })
      .finally(function () {
        findBtn.disabled = false;
      });
  }

  findBtn.addEventListener("click", function () {
    if (!navigator.geolocation) {
      setStatus("This browser cannot share your location. Pick a suburb instead.", true);
      showManualPicker();
      return;
    }

    setStatus("Asking for your location…");

    navigator.geolocation.getCurrentPosition(
      function (position) {
        search(position.coords.latitude, position.coords.longitude);
      },
      function (error) {
        // Denied, unavailable or timed out — the suburb picker is the way out.
        var reason = error.code === error.PERMISSION_DENIED
          ? "Location permission was denied."
          : "Could not get your location.";
        setStatus(reason + " Pick your suburb instead.", true);
        showManualPicker();
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  });

  suburbBtn.addEventListener("click", function () {
    var value = suburbSelect.value;
    if (!value) {
      setStatus("Choose a suburb first.", true);
      return;
    }
    var parts = value.split(",");
    search(parseFloat(parts[0]), parseFloat(parts[1]));
  });

  // Re-run the last search when the filter changes, so the list stays honest.
  onlyFree.addEventListener("change", function () {
    if (lastPosition) {
      search(lastPosition.lat, lastPosition.lng);
    }
  });
})();
