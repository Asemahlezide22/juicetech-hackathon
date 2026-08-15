/* Ask Juice — the AI concierge, in a floating panel.

   Answers come from /api/ai/chat, which redacts the message before it goes
   anywhere and grounds the reply in our published policy documents. When
   something is stripped, we say so in the thread rather than hiding it. */

(function () {
  "use strict";

  var fab = document.getElementById("chat-fab");
  var panel = document.getElementById("chat-panel");
  var form = document.getElementById("chat-form");
  var input = document.getElementById("chat-input");
  var log = document.getElementById("chat-log");
  var lang = document.getElementById("chat-lang");
  var suggests = document.getElementById("chat-suggests");

  if (!fab || !panel || !form) return;

  var busy = false;

  function open() {
    panel.hidden = false;
    fab.classList.add("is-open");
    fab.setAttribute("aria-expanded", "true");
    input.focus();
  }

  function close() {
    panel.hidden = true;
    fab.classList.remove("is-open");
    fab.setAttribute("aria-expanded", "false");
  }

  fab.addEventListener("click", function () {
    if (panel.hidden) open(); else close();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panel.hidden) close();
  });

  /** Append a message bubble and scroll to it. */
  function bubble(text, who, extraClass) {
    var el = document.createElement("div");
    el.className = "chat-msg from-" + who + (extraClass ? " " + extraClass : "");
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  function ask(question) {
    if (busy || !question) return;
    busy = true;

    if (suggests) suggests.remove();

    bubble(question, "me");
    input.value = "";

    var thinking = bubble("…", "bot", "is-thinking");

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
        thinking.remove();
        bubble(data.reply, "bot");

        // Make the redaction visible. This is the point of it.
        if (data.redacted && data.redacted.length) {
          bubble(
            "Stripped before sending: " + data.redacted.join(", ") +
              ". Your details never left this machine.",
            "bot",
            "is-redacted"
          );
        }
      })
      .catch(function (err) {
        thinking.remove();
        bubble(err.message, "bot", "is-error");
      })
      .finally(function () {
        busy = false;
        input.focus();
      });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    ask(input.value.trim());
  });

  if (suggests) {
    suggests.addEventListener("click", function (e) {
      if (e.target.tagName === "BUTTON") ask(e.target.textContent.trim());
    });
  }
})();
