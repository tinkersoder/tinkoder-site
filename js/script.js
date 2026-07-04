/* ============================================================
   TINKODER — script.js
   Vanilla JS only. Handles:
   1. Language preference (remember + redirect from front page)
   2. Dark / light theme with system default
   3. Mobile navigation
   4. Scroll reveal animations
   5. Contact form (client-side demo handler)
   ============================================================ */

(function () {
  "use strict";

  var doc = document.documentElement;
  var PAGE_LANG = doc.lang || "fi"; // each page declares its own lang

  /* ----------------------------------------------------------
     1. LANGUAGE
     - Every page exists in both languages (/, /en/).
     - When the user clicks the language switch we store the
       choice, so the front page can honour it on later visits.
     - Redirect happens ONLY on the site root, only once per
       session, and never against an explicit click — so users
       can always browse either language freely.
  ---------------------------------------------------------- */
  var LANG_KEY = "tinkoder-lang";

  function storedLang() {
    try { return localStorage.getItem(LANG_KEY); } catch (e) { return null; }
  }
  function storeLang(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) { /* private mode */ }
  }

  // Remember the language of the page being viewed via the switch
  document.querySelectorAll("[data-lang-link]").forEach(function (a) {
    a.addEventListener("click", function () {
      storeLang(a.getAttribute("data-lang-link"));
      try { sessionStorage.setItem("tinkoder-lang-manual", "1"); } catch (e) {}
    });
  });

  // Front-page redirect: Finnish root → /en/ if the visitor
  // previously chose English (and vice versa).
  (function langRedirect() {
    var manual = false;
    try { manual = sessionStorage.getItem("tinkoder-lang-manual") === "1"; } catch (e) {}
    if (manual) return;

    var pref = storedLang();
    if (!pref || pref === PAGE_LANG) return;

    var path = location.pathname;
    var isFiRoot = /(^\/$|\/index\.html$)/.test(path) && PAGE_LANG === "fi" && path.indexOf("/en/") === -1;
    var isEnRoot = /\/en\/(index\.html)?$/.test(path) && PAGE_LANG === "en";

    if (pref === "en" && isFiRoot) location.replace("en/index.html");
    if (pref === "fi" && isEnRoot) location.replace("../index.html");
  })();

  // Any visit quietly refreshes the preference to the page language
  // once the user has interacted (scroll/click), so browsing English
  // pages naturally keeps English as the preference.
  window.addEventListener("click", function persistOnce() {
    storeLang(PAGE_LANG);
    window.removeEventListener("click", persistOnce);
  }, { once: true });

  /* ----------------------------------------------------------
     2. THEME (dark / light)
     Default follows the OS. A manual choice is stored and wins.
  ---------------------------------------------------------- */
  var THEME_KEY = "tinkoder-theme";

  function applyTheme(theme) {
    if (theme === "dark") doc.setAttribute("data-theme", "dark");
    else doc.removeAttribute("data-theme");
  }

  var savedTheme = null;
  try { savedTheme = localStorage.getItem(THEME_KEY); } catch (e) {}
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");
  applyTheme(savedTheme || (systemDark.matches ? "dark" : "light"));

  systemDark.addEventListener("change", function (e) {
    if (!savedTheme) applyTheme(e.matches ? "dark" : "light");
  });

  document.querySelectorAll(".theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = doc.getAttribute("data-theme") === "dark" ? "light" : "dark";
      savedTheme = next;
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      applyTheme(next);
    });
  });

  /* ----------------------------------------------------------
     3. MOBILE NAVIGATION
  ---------------------------------------------------------- */
  var burger = document.querySelector(".nav__burger");
  var links = document.querySelector(".nav__links");
  if (burger && links) {
    burger.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // Close the menu after choosing a destination
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ----------------------------------------------------------
     4. SCROLL REVEALS
     Elements with .reveal fade in when they enter the viewport.
     If IntersectionObserver is missing, everything just shows.
  ---------------------------------------------------------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ----------------------------------------------------------
     5. CONTACT FORM
     Front-end demo handler: validates, then shows a success
     message. Wire the fetch() call to your form backend
     (e.g. Formspree, Web3Forms, or your own endpoint) later.
  ---------------------------------------------------------- */
  var form = document.querySelector("#contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var status = form.querySelector(".form__status");
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;

      /* TODO: replace this timeout with a real request, e.g.
         fetch("https://example.com/api/contact", {
           method: "POST",
           body: new FormData(form)
         }) */
      setTimeout(function () {
        form.reset();
        btn.disabled = false;
        status.textContent = status.getAttribute("data-success");
        status.focus && status.focus();
      }, 600);
    });
  }
})();
