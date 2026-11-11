(function () {
  "use strict";

  function all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("[data-toggle]");
    if (toggle) {
      var on = toggle.classList.toggle("is-on");
      toggle.setAttribute("aria-pressed", on ? "true" : "false");
    }

    var segBtn = event.target.closest(".seg__btn");
    if (segBtn) {
      all(".seg__btn", segBtn.closest(".seg")).forEach(function (btn) {
        var active = btn === segBtn;
        btn.classList.toggle("is-on", active);
        btn.setAttribute("aria-pressed", active ? "true" : "false");
      });
    }

    var noteBtn = event.target.closest("[data-demo-note]");
    if (noteBtn) {
      var scope = noteBtn.closest(".phone__sheet") || noteBtn.closest(".panel") || noteBtn.parentElement;
      var note = scope && scope.querySelector("[data-note]");
      if (note) note.textContent = noteBtn.getAttribute("data-demo-note");
    }
  });

  var control = document.querySelector(".control");
  if (control) {
    var revokeButton = control.querySelector("[data-control-revoke]");
    var controlState = control.querySelector("[data-control-state]");
    var authority = control.querySelector("[data-agent-authority]");
    var controlNote = control.querySelector("[data-note]");
    var revoked = false;
    revokeButton.addEventListener("click", function () {
      revoked = !revoked;
      control.classList.toggle("is-revoked", revoked);
      controlState.textContent = revoked ? "Revoked (demo)" : "Active";
      authority.textContent = revoked ? "Revoked (demo)" : "Within limits only";
      revokeButton.textContent = revoked ? "Restore" : "Revoke";
      controlNote.textContent = revoked
        ? "Demo only — authority is shown as revoked; nothing changed."
        : "Demo only — no authority is changed.";
    });
  }

  var phone = document.querySelector('[data-demo="wallet"]');
  if (phone) {
    var views = all(".phone__view", phone);
    var navItems = all("[data-view-target]", phone);
    var sheets = all(".phone__sheet", phone);
    var backdrop = phone.querySelector(".phone__sheet-backdrop");
    var opener = null;

    var setView = function (key) {
      views.forEach(function (view) { view.hidden = view.getAttribute("data-view") !== key; });
      navItems.forEach(function (item) {
        var active = item.getAttribute("data-view-target") === key;
        item.classList.toggle("is-active", active);
        item.setAttribute("aria-pressed", active ? "true" : "false");
      });
    };

    navItems.forEach(function (item) {
      item.addEventListener("click", function () { setView(item.getAttribute("data-view-target")); });
    });

    var closeSheets = function () {
      sheets.forEach(function (sheet) { sheet.hidden = true; });
      if (backdrop) backdrop.hidden = true;
      if (opener && typeof opener.focus === "function") opener.focus();
      opener = null;
    };

    var openSheet = function (name, trigger) {
      var sheet = phone.querySelector('[data-sheet="' + name + '"]');
      if (!sheet) return;
      closeSheets();
      opener = trigger || null;
      sheet.hidden = false;
      if (backdrop) backdrop.hidden = false;
      var focusTarget = sheet.querySelector(".phone__close") || sheet.querySelector("button");
      if (focusTarget) window.setTimeout(function () { focusTarget.focus(); }, 0);
    };

    all("[data-sheet-open]", phone).forEach(function (button) {
      button.addEventListener("click", function () { openSheet(button.getAttribute("data-sheet-open"), button); });
    });
    all("[data-sheet-close]", phone).forEach(function (button) {
      button.addEventListener("click", closeSheets);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && sheets.some(function (sheet) { return !sheet.hidden; })) closeSheets();
    });
    phone.addEventListener("keydown", function (event) {
      if (event.key !== "Tab") return;
      var sheet = sheets.filter(function (item) { return !item.hidden; })[0];
      if (!sheet) return;
      var focusables = all('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])', sheet).filter(function (el) { return !el.disabled; });
      if (!focusables.length) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
  }
})();
