// Only a choice in the language switcher changes the saved language.
(() => {
  const key = "roadbook-ai4pcb:language";
  const config = document.currentScript.dataset;
  try {
    if (document.documentElement.lang === "en" && localStorage.getItem(key) === "zh") {
      const target = new URL(config.chinese, location.href);
      const anchor = decodeURIComponent(location.hash.slice(1));
      const translations = JSON.parse(config.fragments);
      target.search = location.search;
      target.hash = Object.hasOwn(translations, anchor) ? translations[anchor] : location.hash;
      location.replace(target.href);
      return;
    }
  } catch {
    // Static links work when the browser blocks storage or receives a malformed fragment.
  }

  document.addEventListener("click", event => {
    const link = event.target.closest("nav.locales a[lang]");
    if (!link || event.defaultPrevented) return;
    try {
      localStorage.setItem(key, link.lang === "zh-CN" ? "zh" : "en");
    } catch {
      // The language links also work without storage.
    }
  });
})();
