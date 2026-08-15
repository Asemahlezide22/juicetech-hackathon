/* Station dispense / return animation.

   Drives the same markup two ways:
     default              payment -> unlock -> bank slides out
     data-mode="return"   slot opens -> bank slides back in

   Everything is a timed sequence over server-confirmed state. The rental has
   already been updated in the database before this page renders; this only
   shows the customer what the machine is doing. */

(function () {
  "use strict";

  var root = document.querySelector(".k-dispense");
  if (!root) return;

  var isReturn = root.dataset.mode === "return";
  var slotNo = parseInt(root.dataset.slot, 10);

  var authStage = document.getElementById("auth-stage");
  var paidStage = document.getElementById("paid-stage");
  var log = document.getElementById("machine-log");
  var art = document.getElementById("station-art");
  var collect = document.getElementById("collect-stage");
  var targetSlot = art ? art.querySelector('.k-slot[data-slot="' + slotNo + '"]') : null;

  // Honour the OS setting: show the end state immediately, no theatre.
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function show(el) { if (el) el.hidden = false; }
  function hide(el) { if (el) el.hidden = true; }

  function litAll() {
    if (!log) return;
    [].forEach.call(log.children, function (li) { li.classList.add("is-on"); });
  }

  function finish() {
    hide(authStage);
    show(paidStage);
    show(log);
    show(art);
    litAll();

    if (targetSlot) {
      targetSlot.classList.add("is-flashing");
      targetSlot.classList.add(isReturn ? "is-inserting" : "is-empty");
    }
    show(collect);
  }

  if (reduced) {
    finish();
    return;
  }

  // Reveal each machine line in turn.
  function runLog(startDelay, step, done) {
    if (!log) { done(); return; }
    var lines = [].slice.call(log.children);

    lines.forEach(function (li, i) {
      setTimeout(function () {
        li.classList.add("is-on");

        // Unlocking the slot is the moment the hardware reacts.
        if (i === 2 && targetSlot) {
          targetSlot.classList.add("is-flashing");
        }
        // The last line is the bank actually moving.
        if (i === lines.length - 1 && targetSlot) {
          targetSlot.classList.add(isReturn ? "is-inserting" : "is-ejecting");
          if (!isReturn) {
            setTimeout(function () { targetSlot.classList.add("is-empty"); }, 700);
          }
        }
      }, startDelay + i * step);
    });

    setTimeout(done, startDelay + lines.length * step + 700);
  }

  if (isReturn) {
    // No payment stage on a return: the slot opens straight away.
    show(art);
    runLog(400, 900, function () { show(collect); });
    return;
  }

  // "Authorising demo payment…" for about two seconds, then the tick.
  setTimeout(function () {
    hide(authStage);
    show(paidStage);
    show(log);
    show(art);
    runLog(500, 900, function () { show(collect); });
  }, 2000);
})();
