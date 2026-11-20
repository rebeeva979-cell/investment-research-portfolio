(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("mr-lang"); } catch (e) {}
  var q = null;
  try { q = new URLSearchParams(location.search).get("lang"); } catch (e) {}
  var lang = q === "en" || q === "ru" ? q : (saved === "en" || saved === "ru" ? saved : "ru");
  function apply(next) {
    root.setAttribute("data-lang", next);
    root.setAttribute("lang", next);
    document.querySelectorAll("[data-setlang]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", String(btn.getAttribute("data-setlang") === next));
    });
    try { localStorage.setItem("mr-lang", next); } catch (e) {}
  }
  apply(lang);
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-setlang]");
    if (btn) { apply(btn.getAttribute("data-setlang")); }
  });
})();
