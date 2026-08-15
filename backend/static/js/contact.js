/* Enquiry form — posts to the Python API and shows the reference number. */

(function () {
  "use strict";

  var form = document.getElementById("enquiry-form");
  var statusEl = document.getElementById("form-status");
  var submitBtn = form.querySelector('button[type="submit"]');

  function setStatus(message, kind) {
    statusEl.textContent = message;
    statusEl.className = "form-status" + (kind ? " " + kind : "");
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    // Let the browser's own validation speak first.
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var data = new FormData(form);
    var payload = {
      name: data.get("name").trim(),
      email: data.get("email").trim(),
      phone: data.get("phone").trim(),
      message: data.get("message").trim(),
    };

    // The API treats these as optional; empty strings would fail validation.
    if (data.get("event_type")) payload.event_type = data.get("event_type");
    if (data.get("event_date")) payload.event_date = data.get("event_date");

    submitBtn.disabled = true;
    setStatus("Sending…");

    fetch("/api/enquiries", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then(function (response) {
        return response.json().then(function (body) {
          return { ok: response.ok, status: response.status, body: body };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          // FastAPI returns `detail` as a string, or a list for validation errors.
          var detail = result.body && result.body.detail;
          if (Array.isArray(detail)) {
            detail = detail
              .map(function (d) { return d.loc[d.loc.length - 1] + ": " + d.msg; })
              .join(", ");
          }
          throw new Error(detail || "Could not send that (" + result.status + ").");
        }

        form.reset();
        setStatus(
          "Thank you. Your reference is " + result.body.reference +
          " — we'll be in touch.",
          "ok"
        );
      })
      .catch(function (error) {
        setStatus(error.message, "error");
      })
      .finally(function () {
        submitBtn.disabled = false;
      });
  });
})();
