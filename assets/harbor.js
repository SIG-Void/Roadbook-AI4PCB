(function () {
  const viewer = document.querySelector(".harbor-viewer");
  if (!viewer) return;
  const zh = viewer.dataset.lang === "zh";
  const directory = viewer.querySelector(".hb-directory");
  const tree = viewer.querySelector(".hb-tree");
  const files = new Map(Array.from(tree.querySelectorAll("[data-file]"), link => [link.dataset.file, link]));
  const folders = Array.from(tree.querySelectorAll(".hb-folder")).reverse();
  const shortcutLinks = viewer.querySelectorAll("[data-shortcut]");
  const filter = viewer.querySelector("input[type=search]");
  const count = viewer.querySelector(".hb-count");
  const pane = viewer.querySelector(".hb-pane");
  const code = pane.querySelector("code");
  const pre = code.parentElement;
  const image = pane.querySelector(".hb-image");
  const message = pane.querySelector(".hb-message");
  const retry = pane.querySelector(".hb-retry");
  const copy = viewer.querySelector(".hb-copy");
  const download = viewer.querySelector(".hb-download");
  const notice = viewer.querySelector(".hb-notice");
  const mobile = window.matchMedia("(max-width: 700px)");
  let selection = viewer.querySelector(".hb-path").textContent;
  let request;
  let openBeforeFilter = null;
  let copyTimer;

  if (mobile.matches) directory.open = false;
  filter.parentElement.hidden = false;
  copy.hidden = false;

  filter.addEventListener("input", () => {
    const term = filter.value.trim().toLowerCase();
    if (term && !openBeforeFilter) {
      openBeforeFilter = new Set(folders.filter(item => item.firstElementChild.open));
    }
    let matches = 0;
    for (const [path, link] of files) {
      const matched = path.toLowerCase().includes(term);
      link.parentElement.hidden = !matched;
      if (matched) matches++;
    }
    for (const folder of folders) {
      const details = folder.firstElementChild;
      folder.hidden = term && !Array.from(details.querySelector("ul").children).some(child => !child.hidden);
      if (term && !folder.hidden) details.open = true;
      if (!term && openBeforeFilter) details.open = openBeforeFilter.has(folder);
    }
    if (!term) openBeforeFilter = null;
    count.textContent = zh ? matches + " 个文件" : matches + (matches === 1 ? " file" : " files");
  });

  function showMessage(text) {
    message.textContent = text;
    message.hidden = false;
  }

  async function showFile(path) {
    const link = files.get(path);
    if (!link) return;
    if (request) request.abort();
    request = new AbortController();
    const signal = request.signal;
    selection = path;
    clearTimeout(copyTimer);
    copy.textContent = zh ? "复制" : "Copy";
    copy.disabled = true;
    notice.textContent = "";
    for (const other of [...files.values(), ...shortcutLinks]) {
      if ((other.dataset.file || other.dataset.shortcut) === path) other.setAttribute("aria-current", "true");
      else other.removeAttribute("aria-current");
    }
    viewer.querySelector(".hb-path").textContent = path;
    viewer.querySelector(".hb-size").textContent = link.dataset.size;
    download.href = link.href;
    download.download = link.textContent.trim();
    code.textContent = "";
    pre.hidden = true;
    image.hidden = true;
    image.removeAttribute("src");
    message.hidden = true;
    retry.hidden = true;
    pane.scrollTop = 0;
    pane.scrollLeft = 0;

    if (link.dataset.kind === "image") {
      image.alt = path;
      image.src = link.href;
      image.hidden = false;
      return;
    }
    if (link.dataset.kind !== "text") {
      showMessage(zh ? "请下载此文件，在本地打开。" : "Download this file to open it locally.");
      return;
    }
    showMessage(zh ? "正在读取文件…" : "Loading file…");
    try {
      const response = await fetch(link.href, {signal});
      if (!response.ok) throw new Error("Could not load file");
      const text = await response.text();
      if (signal.aborted) return;
      code.textContent = text;
      pre.hidden = false;
      message.hidden = true;
      copy.disabled = false;
    } catch (error) {
      if (signal.aborted) return;
      showMessage(zh ? "文件读取失败。" : "Could not load this file.");
      retry.hidden = false;
    }
  }

  viewer.addEventListener("click", event => {
    const link = event.target.closest("a[data-file], a[data-shortcut]");
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    if (mobile.matches && link.dataset.file) {
      directory.open = false;
      pane.focus({preventScroll: true});
    }
    showFile(link.dataset.file || link.dataset.shortcut);
  });
  retry.addEventListener("click", () => showFile(selection));

  copy.addEventListener("click", async () => {
    const requested = selection;
    try {
      await navigator.clipboard.writeText(code.textContent);
      if (selection !== requested) return;
      copy.textContent = zh ? "已复制" : "Copied";
      notice.textContent = copy.textContent;
      clearTimeout(copyTimer);
      copyTimer = window.setTimeout(() => { copy.textContent = zh ? "复制" : "Copy"; }, 1800);
    } catch {
      if (selection !== requested) return;
      const range = document.createRange();
      range.selectNodeContents(code);
      const current = window.getSelection();
      current.removeAllRanges();
      current.addRange(range);
      showMessage(zh ? "已选中文件内容。请使用系统的复制命令。" : "File text selected. Use the system copy command.");
      pane.focus({preventScroll: true});
    }
  });
})();
