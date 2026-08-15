/* "Ask Juice" — the customer assistant on the AI Operations page.

   The redaction happens on the server, before anything is sent onward. This
   only displays what came back, including what was stripped, so the claim is
   visible rather than asserted. */

(function () {
  "use strict";

  var form = document.getElementById("ai-chat");
  if (!form) return;

  var input = document.getElementById("q");
  var lang = document.getElementById("lang");
  var wrap = document.getElementById("ai-answer");
  var reply = document.getElementById("ai-reply");
  var redacted = document.getElementById("ai-redacted");
  var sourcesWrap = document.getElementById("ai-sources-wrap");
  var sources = document.getElementById("ai-sources");
  var button = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var question = input.value.trim();
    if (!question) return;

    button.disabled = true;
    wrap.hidden = false;
    reply.textContent = "Thinking…";
    redacted.hidden = true;
    sourcesWrap.hidden = true;

    fetch("/api/ai/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question, language: lang.value }),
    })
      .then(function (r) {
        if (!r.ok) throw new Error("Assistant unavailable (" + r.status + ")");
        return r.json();
      })
      .then(function (data) {
        reply.textContent = data.reply;

        if (data.redacted && data.redacted.length) {
          redacted.hidden = false;
          redacted.textContent =
            "Stripped before sending: " + data.redacted.join(", ") +
            ". What actually left this machine: “" + data.sent_to_model + "”";
        }

        if (data.sources && data.sources.length) {
          sources.innerHTML = "";
          data.sources.forEach(function (passage) {
            var p = document.createElement("p");
            p.className = "ai-source";
            p.textContent = passage;
            sources.appendChild(p);
          });
          sourcesWrap.hidden = false;
        }
      })
      .catch(function (error) {
        reply.textContent = error.message;
      })
      .finally(function () {
        button.disabled = false;
      });
  });
})();
