"""Check the built site using only repository files. Run after scripts/build.py."""
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OLD_CONTACTS = ("dengjiajicarl", "dengjiaji@")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_target(source, address):
    link = urlsplit(address)
    require(link.scheme != "file", f"{source.relative_to(DIST)}: local filesystem URL {address}")
    if link.scheme or link.netloc:
        return None
    path = unquote(link.path)
    label = source.relative_to(DIST)
    require(not path.startswith("/"), f"{label}: root-relative link {address}")
    target = (source.parent / path).resolve() if path else source
    require(target.is_relative_to(DIST), f"{label}: link outside site {address}")
    if target.is_dir():
        target /= "index.html"
    require(target.is_file(), f"{label}: missing {address}")
    return target, unquote(link.fragment)


def verify():
    require(DIST.is_dir(), "dist/ is missing. Run python scripts/build.py first.")
    documents = {path: BeautifulSoup(path.read_bytes(), "html.parser", from_encoding="utf-8")
                 for path in sorted(DIST.rglob("*.html"))}
    legacy_root = DIST / "en"
    pages = {path: doc for path, doc in documents.items() if doc.select_one("main#main")}
    home = DIST / "index.html"
    require(home in pages, "The default English homepage is missing.")
    require(DIST / "zh/index.html" in pages, "The Chinese homepage is missing.")
    anchors = {}
    for path, doc in pages.items():
        ids = [item["id"] for item in doc.select("[id]")]
        require(len(ids) == len(set(ids)), f"{path.relative_to(DIST)}: duplicate HTML id")
        anchors[path] = set(ids)

    def check_link(path, address):
        result = local_target(path, address)
        if result:
            target, fragment = result
            if fragment and target in pages:
                require(fragment in anchors[target], f"{path.relative_to(DIST)}: missing anchor {address}")
            return target
        return None

    aliases = set(documents) - set(pages)
    english_pages = {path for path in pages if not path.is_relative_to(DIST / "zh")}
    expected_redirects = {legacy_root / path.relative_to(DIST): (path, "") for path in english_pages}
    for prefix in ("", "zh", "en"):
        lang_root = DIST / "zh" if prefix == "zh" else DIST
        for topic in ("footprints", "layout", "fabrication"):
            old_page = DIST / prefix / "design" / topic / "index.html"
            expected_redirects[old_page] = (lang_root / "design/review/index.html", topic)
    require(aliases == set(expected_redirects), "Redirect coverage differs from published legacy routes")
    for path in sorted(aliases):
        doc = documents[path]
        target, section = expected_redirects[path]
        canonical = doc.select_one('link[rel~="canonical"][href]')
        refresh = doc.find("meta", attrs={"http-equiv": re.compile(r"^refresh$", re.I)})
        match = re.fullmatch(r"0\s*;\s*url\s*=\s*(.+)", refresh.get("content", ""), re.I) if refresh else None
        require(doc.html.get("lang") == pages[target].html["lang"] and canonical and match,
                f"{path.relative_to(DIST)}: invalid redirect or missing canonical")
        require(urlsplit(match[1]).fragment == section, f"{path}: incorrect landing section")
        for address in [canonical["href"], match[1].strip("'\" ")]:
            if urlsplit(address).netloc:
                primary = pages[target].select_one('link[rel~="canonical"][href]')
                require(primary and address == primary["href"], f"{path.relative_to(DIST)}: wrong absolute destination")
            else:
                require(check_link(path, address) == target, f"{path.relative_to(DIST)}: wrong redirect destination")

    for path, doc in pages.items():
        rel = path.relative_to(DIST)
        for tag in doc.select("[href], [src], [srcset]"):
            for attr in ("href", "src"):
                if tag.has_attr(attr):
                    check_link(path, tag[attr])
            for candidate in tag.get("srcset", "").split(","):
                if candidate.strip():
                    check_link(path, candidate.split()[0])
        english = rel.parts[0] != "zh"
        suffix = rel if english else Path(*rel.parts[1:])
        targets = {"zh-CN": DIST / "zh" / suffix, "en": DIST / suffix}
        current = "en" if english else "zh-CN"
        require(doc.html.get("lang") == current, f"{rel}: wrong document language")
        links = {a.get("lang"): a for a in doc.select("nav.locales a")}
        require(links.keys() == targets.keys(), f"{rel}: missing language switch")
        for lang, target in targets.items():
            require(target in pages and check_link(path, links[lang]["href"]) == target,
                    f"{rel}: wrong {lang} language destination")
        require(links[current].get("aria-current") == "true", f"{rel}: active language missing")
        fragments = json.loads(doc.select_one("script#site-language")["data-fragments"])
        alternate = targets["zh-CN" if english else "en"]
        require(set(fragments) <= anchors[path] and set(fragments.values()) <= anchors[alternate],
                f"{rel}: unresolved translated fragment")
        require(not doc.select_one('footer .source-links, footer a[download], footer a[href*="/edit/"]'),
                f"{rel}: obsolete footer action")
        require(doc.select_one("footer .colophon").get_text(strip=True) == "Roadbook AI4PCB",
                f"{rel}: unexpected footer text")
        repository = doc.select_one('.top-link[href^="https://github.com/"]')
        if repository:
            contribute = doc.select_one("#directory .rail-note")
            require(contribute and contribute["href"] == repository["href"] + "/compare",
                    f"{rel}: missing pull request link")
        directory = [check_link(path, a["href"]) for a in doc.select("#directory section li a")]
        require(path in directory and directory.count(path) == 1, f"{rel}: page missing or duplicated in navigation")
        for branch in doc.select("#directory li.nav-branch"):
            folder = branch.find("details", recursive=False)
            require(folder and folder.find("summary", recursive=False) and folder.select_one("ul a[href]"),
                    f"{rel}: missing navigation folder control or links")
            current_child = folder.select_one('a[aria-current="page"]') is not None
            require(folder.has_attr("open") == current_child, f"{rel}: incorrect initial folder state")
        position = directory.index(path)
        neighbours = directory[max(0, position - 1):position] + directory[position + 1:position + 2]
        require([check_link(path, a["href"]) for a in doc.select("nav.pager a")] == neighbours,
                f"{rel}: previous/next pages differ from the directory order")

    for css in DIST.rglob("*.css"):
        for link in re.findall(r"""url\(\s*['"]?([^'")\s]+)['"]?\s*\)""", css.read_text()):
            check_link(css, link)
    for path in DIST.rglob("*"):
        if path.suffix in {".html", ".md", ".json", ".js", ".svg"}:
            body = path.read_text().casefold()
            require(not any(token in body for token in OLD_CONTACTS),
                    f"{path.relative_to(DIST)}: contact from reference site")

    result_count = 0
    for lang, paper_heading, start_heading in (
        ("zh", "AI × PCB 论文精选", "从哪里开始"), ("en", "Selected AI × PCB papers", "Where to start")
    ):
        lang_root = DIST if lang == "en" else DIST / "zh"
        start = lang_root / "index.html"
        workflow = lang_root / "workflow" / "index.html"
        paper_page = lang_root / "research/papers/index.html"
        doc = pages[start]
        first = doc.select_one("article h2")
        require(first and first.get_text(strip=True) == paper_heading, f"{lang}: papers must lead the homepage")
        first_list = first.find_next_sibling()
        require(first_list and first_list.name == "ul" and first_list.select("li a[href]"),
                f"{lang}: no papers under the featured heading")
        sections = {section.h2.get_text(strip=True): section for section in doc.select("#directory section")}
        require(list(sections) == ["Overview", "AI Model", "PCB", "Field Notes", "Community"],
                f"{lang}: incorrect navigation groups")
        def section_pages(group):
            return [check_link(start, link["href"]) for link in sections[group].select("li a")]
        require(section_pages("Overview") == [start], f"{lang}: incorrect Overview entry")
        harbor = lang_root / "research/harbor-examples/index.html"
        require(section_pages("AI Model")[-1] == harbor, f"{lang}: missing Harbor example after training")
        viewer = pages[harbor].select_one(".harbor-viewer")
        require(viewer and viewer["data-lang"] == lang, f"{lang}: wrong language for the Harbor controls")
        require(viewer.select_one(".hb-copy").get_text(strip=True) == ("复制" if lang == "zh" else "Copy"),
                f"{lang}: missing localized file controls")
        shortcuts = {a["data-shortcut"]: check_link(harbor, a["href"]) for a in viewer.select("[data-shortcut]")}
        require(set(shortcuts) == {"instruction.md", "README.md"}, f"{lang}: incorrect default task files")
        for filename, path in shortcuts.items():
            heading = path.read_text(encoding="utf-8").splitlines()[0]
            require(path.name == filename and re.match(r"^#\s+[A-Za-z]", heading) and not re.search(r"[\u3400-\u9fff]", heading),
                    f"{lang}: missing English task document {filename}")
        require(viewer.select_one(".hb-path").get_text(strip=True) == "instruction.md"
                and viewer.select_one(".hb-code[lang=en] code").get_text() == shortcuts["instruction.md"].read_text(encoding="utf-8"),
                f"{lang}: initial preview must match the English instruction file")
        design_pages = [lang_root / "design" / name / "index.html" for name in ("tools", "review", "boards")]
        require(section_pages("PCB") == [workflow, *design_pages], f"{lang}: incorrect PCB navigation")
        require(all(figure.select_one("a[href]") and figure.select_one("img[alt]") for figure in pages[workflow].select("figure"))
                and pages[workflow].select_one("figure"), f"{lang}: missing linked workflow illustrations")
        featured = pages[lang_root / "research/benchmarks/index.html"]
        benchmark_sections = [node["id"] for node in featured.select("article h2")]
        require(benchmark_sections[:3] == ["ale", "omnilayout", "benchcad-t6"],
                f"{lang}: incorrect benchmark order")
        require(not doc.select_one(".heading.home .stats"), f"{lang}: obsolete homepage counters")
        require(int(featured.select_one(".kicker span").get_text(strip=True).split()[0]) == len(benchmark_sections),
                f"{lang}: wrong benchmark count on the benchmark page")
        blog_index = pages[lang_root / "blog/index.html"]
        article_links = blog_index.select("article p a")
        expected_notes = {p for p in pages if p.parent.parent == lang_root / "blog"}
        require({check_link(lang_root / "blog/index.html", a["href"]) for a in article_links} == expected_notes,
                f"{lang}: the blog index must list every article")
        for link in article_links:
            target = check_link(lang_root / "blog/index.html", link["href"])
            article = pages[target]
            figures = article.select("figure")
            require(figures, f"{target}: missing illustration")
            for figure in figures:
                image = figure.select_one("img[alt]")
                require(image and image["alt"].strip(), f"{target}: missing illustration description")
                require(figure.select_one("figcaption a[download]"), f"{target}: missing editable figure")
                if urlsplit(image["src"]).path.endswith(".svg"):
                    still = figure.select_one('picture source[media="(prefers-reduced-motion: reduce)"]')
                    require(still and still["srcset"] == image["src"] + "#still", f"{target}: missing static figure")
                    drawing = ElementTree.parse(check_link(target, image["src"])).getroot()
                    require(drawing.get("viewBox") and all(drawing.get(axis, "100%") == "100%" for axis in ("width", "height")),
                            f"{target}: the full-size SVG must fit the browser window")
        heading = doc.find("h2", string=start_heading)
        table = heading.find_next_sibling() if heading else None
        link = table.select_one("tbody tr:first-child td:nth-child(2) a") if table and table.name == "table" else None
        require(link and check_link(start, link["href"]) == workflow, f"{lang}: first reading route must open workflow")
        desktop_sections = [a["href"] for a in pages[workflow].select(".contents a")]
        mobile_sections = [a["href"] for a in pages[workflow].select(".inline-toc a")]
        require(mobile_sections and mobile_sections == desktop_sections, f"{lang}: missing mobile workflow chapters")
        search_json = (DIST / f"search-{lang}.json").read_text()
        require("<" not in search_json, f"{lang}: unsafe HTML delimiter in the search index")
        index = json.loads(search_json)
        paper_entries = {row["anchor"]: row for row in index
                         if row.get("anchor") and row["url"].split("#")[0].endswith("research/papers/")}
        for link in pages[paper_page].select("article li[id] a[title]:first-child"):
            row = paper_entries[link.find_parent("li")["id"]]
            require(row.get("paper_title") == link["title"], f"{lang}: missing full title for {row['label']}")
            if link["href"].startswith("https://arxiv.org/abs/"):
                require(row.get("identifier") == "arXiv:" + link["href"].rsplit("/", 1)[-1], f"{lang}: missing arXiv ID")
        indexed = set()
        for item in index:
            require(item["label"].strip(), f"{lang}: empty search label")
            target = check_link(home, item["url"])
            require(target in pages and pages[target].body["data-locale"] == lang,
                    f"{lang}: search result points outside its language: {item['url']}")
            if target == paper_page:
                require(item["label"].lower() not in {"论文", "paper", "会议摘要", "abstract"},
                        f"{lang}: unnamed paper in search index")
            indexed.add(target)
        expected = {path for path, page in pages.items() if page.body["data-locale"] == lang}
        for path in expected:
            block = pages[path].select_one('script#search-index[type="application/json"]:not([src])')
            require(block and block.string == search_json, f"{path.relative_to(DIST)}: inline search index differs from search-{lang}.json")
        require(indexed == expected, f"{lang}: search index does not cover every page")
        result_count += len(index)

    require(not (DIST / "source").exists(), "Obsolete Markdown downloads in the published site")
    print(f"Verified {len(pages)} pages, {len(aliases)} legacy redirects, {result_count} search results, links and languages.")


if __name__ == "__main__":
    verify()
