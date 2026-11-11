(function () {
  "use strict";

  var narrative = document.querySelector("[data-narrative]");
  if (!narrative) return;

  var stage = narrative.querySelector("[data-stage]");
  if (!stage) return;

  var chapters = Array.prototype.slice.call(narrative.querySelectorAll("[data-chapter]"));
  var rails = Array.prototype.slice.call(narrative.querySelectorAll("[data-rail]"));
  var stageLabel = narrative.querySelector("[data-stage-label]");
  var reduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var labels = [
    "00 / FOUNDATION",
    "01 / ACCESS",
    "02 / INTELLIGENCE",
    "03 / EXECUTION",
    "04 / OVERSIGHT",
    "05 / ONE SYSTEM"
  ];

  var phaseNames = ["INPUTS", "CONSOLIDATE", "ALLOCATE", "PERFORM", "MONITOR"];
  var offsets = [];
  var active = -1;
  var phase = -1;
  var ticking = false;

  function measure() {
    var base = window.scrollY;
    offsets = chapters.map(function (chapter) {
      var rect = chapter.getBoundingClientRect();
      return {
        top: rect.top + base,
        height: rect.height,
        act: parseInt(chapter.getAttribute("data-chapter"), 10),
        el: chapter
      };
    });
  }

  function setActive(act, progress) {
    if (act !== active) {
      active = act;
      phase = -1;
      stage.setAttribute("data-act", String(act));
      stage.removeAttribute("data-phase");
      if (stageLabel) stageLabel.textContent = labels[act] || labels[0];
      rails.forEach(function (link) {
        var on = link.getAttribute("data-rail") === String(act);
        link.classList.toggle("is-active", on);
        if (on) link.setAttribute("aria-current", "step");
        else link.removeAttribute("aria-current");
      });
      chapters.forEach(function (chapter) {
        chapter.classList.toggle(
          "is-active",
          parseInt(chapter.getAttribute("data-chapter"), 10) === act
        );
      });
    }

    var clamped = Math.max(0, Math.min(1, progress));
    if (act === 4) {
      var nextPhase = Math.min(4, Math.floor(clamped * 5));
      if (nextPhase !== phase) {
        phase = nextPhase;
        stage.setAttribute("data-phase", String(nextPhase));
        if (stageLabel) stageLabel.textContent = labels[4] + " · " + phaseNames[nextPhase];
      }
    } else if (phase !== -1) {
      phase = -1;
      stage.removeAttribute("data-phase");
      if (stageLabel) stageLabel.textContent = labels[act] || labels[0];
    }

    stage.style.setProperty("--p", clamped.toFixed(3));
  }

  function update() {
    if (reduce && reduce.matches) {
      phase = -1;
      stage.setAttribute("data-act", "5");
      stage.removeAttribute("data-phase");
      if (stageLabel) stageLabel.textContent = labels[5];
      stage.style.setProperty("--story", "1");
      return;
    }

    var center = window.scrollY + window.innerHeight * 0.55;
    var act = 0;
    var progress = 0;

    for (var i = 0; i < offsets.length; i++) {
      var item = offsets[i];
      if (center >= item.top && center < item.top + item.height) {
        act = item.act;
        progress = (center - item.top) / item.height;
        break;
      }
      if (center >= item.top + item.height) {
        act = item.act;
        progress = 1;
      }
    }

    setActive(act, progress);

    if (offsets.length) {
      var start = offsets[0].top;
      var last = offsets[offsets.length - 1];
      var end = last.top + last.height;
      var story = (center - start) / Math.max(1, end - start);
      stage.style.setProperty("--story", Math.max(0, Math.min(1, story)).toFixed(3));
    }
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      update();
    });
  }

  function refresh() {
    measure();
    update();
  }

  if (reduce && reduce.matches) {
    stage.setAttribute("data-act", "5");
    if (stageLabel) stageLabel.textContent = labels[5];
  }

  refresh();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", refresh);
  window.addEventListener("load", refresh);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
  if (reduce && reduce.addEventListener) reduce.addEventListener("change", refresh);
})();
