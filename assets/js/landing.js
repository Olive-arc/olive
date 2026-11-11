(function () {
  "use strict";

  var nav = document.querySelector(".js-nav");
  var burger = document.querySelector(".nav__burger");
  var burgerLabel = document.querySelector(".nav__burger-label");

  if (nav) {
    var onScroll = function () {
      nav.classList.toggle("nav--solid", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (nav && burger) {
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (burgerLabel) burgerLabel.textContent = open ? "Close" : "Menu";
    };

    burger.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll(".nav__menu a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("click", function (event) {
      if (nav.classList.contains("is-open") && !nav.contains(event.target)) setOpen(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        burger.focus();
      }
    });
  }

  var feature = document.querySelector(".nav__feature");
  var featureTrigger = document.querySelector(".nav__feature-trigger");
  var featurePanel = document.getElementById("nav-features-panel");

  if (feature && featureTrigger && featurePanel) {
    var featureOpen = false;
    var featureOpenTimer = null;
    var featureCloseTimer = null;
    var canHover = window.matchMedia
      ? window.matchMedia("(hover: hover) and (pointer: fine)")
      : null;

    var setFeature = function (open) {
      featureOpen = open;
      featureTrigger.setAttribute("aria-expanded", open ? "true" : "false");
      featurePanel.hidden = !open;
      feature.classList.toggle("is-open", open);
      window.clearTimeout(featureOpenTimer);
      window.clearTimeout(featureCloseTimer);
    };

    var scheduleFeatureOpen = function () {
      window.clearTimeout(featureCloseTimer);
      featureOpenTimer = window.setTimeout(function () {
        setFeature(true);
      }, 90);
    };

    var scheduleFeatureClose = function () {
      window.clearTimeout(featureOpenTimer);
      featureCloseTimer = window.setTimeout(function () {
        setFeature(false);
      }, 160);
    };

    featureTrigger.addEventListener("click", function (event) {
      event.stopPropagation();
      setFeature(!featureOpen);
    });

    feature.addEventListener("pointerenter", function (event) {
      if (event.pointerType === "mouse" && (!canHover || canHover.matches)) {
        scheduleFeatureOpen();
      }
    });

    feature.addEventListener("pointerleave", function (event) {
      if (event.pointerType === "mouse") scheduleFeatureClose();
    });

    feature.addEventListener("focusout", function (event) {
      if (!feature.contains(event.relatedTarget)) setFeature(false);
    });

    document.addEventListener("click", function (event) {
      if (featureOpen && !feature.contains(event.target)) setFeature(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && featureOpen) {
        setFeature(false);
        featureTrigger.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth < 1024) setFeature(false);
    });

    window.addEventListener("scroll", function () {
      if (featureOpen) setFeature(false);
    }, { passive: true });
  }

  var currentFeature = document.body.getAttribute("data-feature");
  if (currentFeature) {
    document.querySelectorAll("[data-feature-link]").forEach(function (link) {
      if (link.getAttribute("data-feature-link") === currentFeature) {
        link.setAttribute("aria-current", "page");
      }
    });
    if (feature) feature.classList.add("has-current");
  }

  var pillarList = document.querySelector("[data-pillar-list]");
  if (pillarList) {
    var pillarItems = Array.prototype.slice.call(
      pillarList.querySelectorAll("details")
    );
    pillarItems.forEach(function (item) {
      item.addEventListener("toggle", function () {
        if (!item.open) return;
        pillarItems.forEach(function (other) {
          if (other !== item) other.open = false;
        });
      });
    });
  }

  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in-view"); });
  }

  document.querySelectorAll("[data-wave]").forEach(function (el) {
    var text = el.textContent;
    el.textContent = "";
    el.setAttribute("tabindex", "0");
    Array.prototype.forEach.call(text, function (ch, i) {
      var span = document.createElement("span");
      span.className = "ch";
      span.textContent = ch === " " ? "\u00A0" : ch;
      span.style.setProperty("--i", i);
      el.appendChild(span);
    });
    var on = function () { el.classList.add("wave--on"); };
    var off = function () { el.classList.remove("wave--on"); };
    el.addEventListener("mouseenter", on);
    el.addEventListener("mouseleave", off);
    el.addEventListener("focus", on);
    el.addEventListener("blur", off);
  });
})();
