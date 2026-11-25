const body = document.body;
const zh = body.dataset.locale === "zh";
const menu = document.querySelector(".menu-toggle");
const rail = document.querySelector(".rail");
const mobile = window.matchMedia("(max-width: 800px)");
const main = document.querySelector("main");
const dialog = document.querySelector("dialog");
const launch = document.querySelector(".search-launch");
const query = document.querySelector("#query");
const statusLine = document.querySelector(".search-status");
const results = document.querySelector(".results");
const resultLimit = 12;
let requestedIndex;
let index = readEmbeddedIndex();
let visibleResults = resultLimit;

function setMenu(open, focus = false) {
  body.classList.toggle("menu-open", open);
  menu.setAttribute("aria-expanded", String(open));
  main.inert = open;
  if (open && focus) {
    const activePage = rail.querySelector("[aria-current=page]");
    const collapsed = activePage.closest("details:not([open])");
    (collapsed ? collapsed.querySelector("summary") : activePage).focus();
  }
  if (!open && focus) menu.focus();
}

menu.addEventListener("click", () => setMenu(!body.classList.contains("menu-open"), true));
document.querySelector(".scrim").addEventListener("click", () => setMenu(false, true));
rail.addEventListener("click", event => {
  if (event.target.closest("a")) setMenu(false);
});
mobile.addEventListener("change", () => setMenu(false));
window.addEventListener("pageshow", () => setMenu(false));

const outline = document.querySelector(".inline-toc");
document.querySelector(".outline-shortcut")?.addEventListener("click", event => {
  event.preventDefault();
  setMenu(false);
  outline.open = true;
  outline.scrollIntoView({block: "start", behavior: "instant"});
  outline.querySelector("summary").focus({preventScroll: true});
});
outline?.addEventListener("click", event => {
  const link = event.target.closest("nav a");
  if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  outline.open = false;
  // Collapsing the list changes the target position. Let native anchor navigation follow.
  const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
  if (target) {
    target.tabIndex = -1;
    target.focus({preventScroll: true});
  }
});

const toc = [...document.querySelectorAll(".contents a")];
const sections = toc.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1))));
let scrollQueued = false;
function markSection() {
  const top = document.querySelector(".mast").offsetHeight + 55;
  let current = 0;
  for (let n = 0; n < sections.length; n++) {
    if (sections[n].getBoundingClientRect().top > top) break;
    current = n;
  }
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 3) current = sections.length - 1;
  toc.forEach((link, i) => {
    if (i === current) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
  scrollQueued = false;
}
if (sections.length) {
  markSection();
  window.addEventListener("scroll", () => {
    if (!scrollQueued) requestAnimationFrame(markSection);
    scrollQueued = true;
  }, {passive: true});
}

const shortcut = /Mac|iPhone|iPad/.test(navigator.platform) ? "⌘ K" : "Ctrl K";
launch.querySelector("kbd").textContent = shortcut;
function readEmbeddedIndex() {
  const block = document.getElementById("search-index");
  if (!block) return;
  try {
    const entries = JSON.parse(block.textContent);
    if (Array.isArray(entries)) return entries;
  } catch {
    // The standalone index also serves older pages and incomplete data blocks.
  }
}

function indexData() {
  if (!requestedIndex) {
    requestedIndex = fetch(body.dataset.root + "search-" + body.dataset.locale + ".json")
      .then(response => {
        if (!response.ok) throw new Error("Search index unavailable");
        return response.json();
      }).catch(error => { requestedIndex = undefined; throw error; });
  }
  return requestedIndex;
}

function field(tag, text) {
  const el = document.createElement(tag);
  el.textContent = text;
  return el;
}

function normalizeSearch(value) {
  return value.normalize("NFKC").toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

function updateResults() {
  results.replaceChildren();
  const term = normalizeSearch(query.value);
  if (!term) {
    statusLine.textContent = zh ? "试试 KiCad、原理图或 PCBWorld。" : "Try KiCad, schematic, or PCBWorld.";
    return;
  }
  if (!index) {
    statusLine.textContent = zh ? "正在读取索引…" : "Loading the index…";
    return;
  }
  const words = term.split(/\s+/);
  const matches = [];
  for (const item of index) {
    const name = normalizeSearch(item.label);
    const title = normalizeSearch(item.paper_title || "");
    const identifiers = normalizeSearch(item.identifier || "");
    const description = normalizeSearch(item.text);
    const page = normalizeSearch(item.page);
    const fields = [name, title, identifiers, description, page].join(" ");
    const exact = name === term || title === term || identifiers === term;
    const compactName = name.replaceAll(" ", "") === term.replaceAll(" ", "");
    if (!compactName && !words.every(word => fields.includes(word))) continue;
    const score = (exact ? 100 : 0) + (compactName ? 20 : 0) +
      words.reduce((sum, word) => sum + (name.includes(word) ? 8 : 0) +
        (title.includes(word) || identifiers.includes(word) ? 5 : 0) +
        (description.includes(word) ? 2 : 0) + (page === word ? 1 : 0), 0);
    matches.push({item, score});
  }
  matches.sort((a, b) => b.score - a.score);
  statusLine.textContent = matches.length
    ? (zh ? "找到 " + matches.length + " 条结果" : matches.length + (matches.length === 1 ? " result" : " results"))
    : (zh ? "没有找到匹配的条目。可以换一个项目名或关键词。" : "No matches. Try a project name or another search term.");
  for (const {item} of matches.slice(0, visibleResults)) {
    const result = document.createElement("li");
    const link = document.createElement("a");
    link.href = body.dataset.root + item.url;
    link.append(field("small", item.page), field("strong", item.label));
    if (item.paper_title) link.append(field("cite", item.paper_title));
    if (item.text) {
      const first = item.text.toLocaleLowerCase().indexOf(words[0]);
      const start = Math.max(0, first - 32);
      const excerpt = (start ? "…" : "") + item.text.slice(start, start + 135) +
        (item.text.length > start + 135 ? "…" : "");
      link.append(field("p", excerpt));
    }
    result.append(link);
    results.append(result);
  }
  if (matches.length > visibleResults) {
    const more = field("button", zh ? "显示更多" : "Show more");
    more.className = "more";
    more.addEventListener("click", () => {
      const firstNew = visibleResults;
      visibleResults += resultLimit;
      updateResults();
      results.querySelectorAll("a")[firstNew]?.focus();
    });
    const row = document.createElement("li");
    row.append(more);
    results.append(row);
  }
}

async function openSearch() {
  if (dialog.open) return;
  setMenu(false);
  dialog.returnValue = "";
  dialog.showModal();
  query.focus();
  query.select();
  updateResults();
  if (index) return;
  try { index = await indexData(); updateResults(); }
  catch { statusLine.textContent = zh ? "搜索暂时不可用。关闭并重新打开可重试。" : "Search is unavailable. Reopen it to retry."; }
}
launch.addEventListener("click", openSearch);
document.querySelector(".escape").addEventListener("click", () => dialog.close());
dialog.addEventListener("close", () => {
  if (dialog.returnValue !== "navigate") launch.focus({preventScroll: true});
});
dialog.addEventListener("click", event => {
  const link = event.target.closest(".results a");
  if (link) {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    dialog.close("navigate");
    if (link.pathname === location.pathname && link.search === location.search && link.hash) {
      const section = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      if (section) requestAnimationFrame(() => {
        section.tabIndex = -1;
        section.focus({preventScroll: true});
        section.scrollIntoView({block: "start", behavior: "instant"});
      });
    }
    return;
  }
  if (event.target !== dialog) return;
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});
query.addEventListener("input", () => { visibleResults = resultLimit; updateResults(); });
dialog.addEventListener("keydown", event => {
  if (event.isComposing || event.keyCode === 229) return;
  if (event.key === "Escape") {
    event.preventDefault();
    dialog.close();
    return;
  }
  if (!["ArrowDown", "ArrowUp", "Enter"].includes(event.key)) return;
  const links = [...results.querySelectorAll("a")];
  if (!links.length) return;
  if (event.key === "Enter" && document.activeElement === query) { event.preventDefault(); links[0].click(); }
  if (event.key === "ArrowDown" || event.key === "ArrowUp") {
    event.preventDefault();
    const i = links.indexOf(document.activeElement) + (event.key === "ArrowDown" ? 1 : -1);
    (i < 0 ? query : links[Math.min(i, links.length - 1)]).focus();
  }
});
document.addEventListener("keydown", event => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault(); openSearch();
  }
  if (event.key === "Escape" && body.classList.contains("menu-open")) setMenu(false, true);
});

const localeBar = document.querySelector(".locales");
const alternate = localeBar.querySelector("a:not([aria-current])");
const alternatePage = new URL(alternate.href);
alternatePage.search = location.search;
const translatedAnchors = JSON.parse(document.querySelector("#site-language")?.dataset.fragments || localeBar.dataset.fragments || "{}");
function updateAlternateLink() {
  let anchor = "";
  try { anchor = decodeURIComponent(location.hash.slice(1)); }
  catch { /* Unknown fragments still lead to the translated page. */ }
  const translated = Object.hasOwn(translatedAnchors, anchor) ? translatedAnchors[anchor] : "";
  alternatePage.hash = translated || "";
  alternate.href = alternatePage.href;
}
// Old unprefixed links can contain a Chinese chapter name.
if (!zh && location.hash) {
  let sharedAnchor;
  try { sharedAnchor = decodeURIComponent(location.hash.slice(1)); } catch { /* Invalid URL fragment. */ }
  if (sharedAnchor && !document.getElementById(sharedAnchor)) {
    const section = Object.keys(translatedAnchors).find(id => translatedAnchors[id] === sharedAnchor);
    const target = section && document.getElementById(section);
    if (target) {
      const next = new URL(location.href);
      next.hash = section;
      history.replaceState(history.state, "", next.href);
      target.scrollIntoView({block: "start"});
    }
  }
}
updateAlternateLink();
window.addEventListener("hashchange", updateAlternateLink);
