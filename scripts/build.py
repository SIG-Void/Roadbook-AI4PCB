"""Build the bilingual static site. All site links work under any Pages subpath."""
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from itertools import groupby
from operator import attrgetter
from pathlib import Path
from urllib.parse import urlsplit

import mistune
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from harbor_example import load_example
from workflow_figures import insert_workflow_figures

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
LANGUAGES = ("zh", "en")
MERGED_DESIGN_TOPICS = ("footprints", "layout", "fabrication")
MARKDOWN = mistune.create_markdown(escape=False, plugins=["table"])
ENV = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]),
                  undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)


@dataclass(frozen=True)
class Page:
    key: str
    route: str
    group: str
    zh: str
    en: str
    nav_zh: str = ""
    nav_en: str = ""
    subsection: tuple = ()

    def nav_title(self, lang):
        return (self.nav_zh if lang == "zh" else self.nav_en) or self.title(lang)

    def title(self, lang):
        return self.zh if lang == "zh" else self.en

    def folder(self, lang):
        return "/".join(part for part in ("zh" if lang == "zh" else "", self.route) if part)


DATASETS = ("数据集", "Datasets")
PAGES = [
    Page("home", "", "Overview", "Roadbook AI4PCB", "Roadbook AI4PCB"),
    Page("papers", "research/papers", "AI Model", "论文精选", "Selected papers"),
    Page("benchmarks", "research/benchmarks", "AI Model", "评测基准", "Benchmarks"),
    Page("data", "research/datasets", "AI Model", "开源与公开数据集", "Open and public datasets", subsection=DATASETS),
    Page("data-procurement", "research/datasets/procurement", "AI Model", "怎样判断原始 PCB 数据的质量？", "How to check the quality of PCB design files",
         "原始 PCB 数据质量", "PCB design file quality", subsection=DATASETS),
    Page("models", "research/models", "AI Model", "模型与权重", "Models and weights"),
    Page("agents", "research/agents", "AI Model", "KiCad 智能体与插件", "KiCad agents and plugins"),
    Page("training", "research/training", "AI Model", "训练与复现", "Training and reproduction"),
    Page("harbor", "research/harbor-examples", "AI Model", "Harbor 环境示例", "Harbor environment example"),
    Page("workflow", "workflow", "PCB", "PCB 绘制流程", "PCB design workflow"),
    Page("tools", "design/tools", "PCB", "工具与环境", "Tools and environments"),
    Page("design-review", "design/review", "PCB", "从封装到投板的设计审查", "Board design review", "设计审查与交付", "Review and handoff"),
    Page("boards", "design/boards", "PCB", "公开板卡", "Reference boards"),
    Page("blog", "blog", "Field Notes", "工程博客", "Engineering blog"),
    Page("design-checks", "blog/design-checks", "Field Notes", "设计规则通过了，安装孔距也对吗？", "Do the mounting holes match the enclosure after the design checks pass?", "检查安装孔距", "Check mounting hole spacing"),
    Page("assembly-origin", "blog/assembly-origin", "Field Notes", "贴片坐标变了，元件移动了吗？", "Did the part move, or did its placement coordinates change?", "核对贴片坐标", "Check placement coordinates"),
    Page("rp2040-power", "blog/rp2040-power", "Field Notes", "网名相同，电源脚就接通了吗？", "Do power pins on the same net have a copper connection?", "检查电源脚的连接", "Trace a power connection"),
    Page("revision-task", "blog/revision-task", "Field Notes", "电压读数为什么会偏？看 Glasgow 的一次改版", "Why did the voltage reading change on the Glasgow board?", "查电压读数偏差", "Investigate voltage readings"),
    Page("routing-scores", "blog/routing-scores", "Field Notes", "平均接通了 94.9%，为什么十块板只有四块通过？", "Why did only four of ten boards pass at 94.9% average routing completion?", "读懂布线通过率", "Read routing scores"),
    Page("board-family-split", "blog/board-family-split", "Field Notes", "同一款板改了版，能用来测试模型吗？", "Can two revisions of one board test a model on a new design?", "选择独立的测试板", "Select independent test boards"),
    Page("about", "about", "Community", "贡献与合作", "Contribute and collaborate"),
]
BY_KEY = {page.key: page for page in PAGES}
CATALOG = {"papers", "benchmarks", "data", "models", "agents", "tools", "boards"}
DESCRIPTIONS = {
    "home": ("AI 与 PCB 设计的论文、评测、数据集和开源项目。", "Research, benchmarks, datasets, and tools for AI in PCB design."),
    "workflow": ("SIGVoid 团队硬件工程师手写的绘板笔记，记录一块 PCB 从确定需求、画原理图，到布局、布线和打样前检查的过程。", "A SIGVoid hardware engineer wrote these notes on PCB design, from requirements and schematics through placement, routing, and checks before fabrication."),
    "boards": ("用真实工程对照原理图、板文件和机械约束。", "Compare schematics, board files, and mechanical constraints in published designs."),
    "about": ("与 SIGVoid 的硬件工程师和研究员一起整理 AI 在 PCB 设计中的研究和实践。", "Help SIGVoid hardware engineers and researchers maintain this guide to AI in PCB design."),
}


def relative(source, target):
    return posixpath.relpath(target or ".", source or ".")


def page_link(page, lang, source):
    path = relative(source, page.folder(lang))
    return "./" if path == "." else path + "/"


def slug(text):
    return re.sub(r"[^\w\-]+", "-", text.casefold()).strip("-") or "section"


def read_page(page, lang, figure_versions):
    source = ROOT / "content" / lang / (page.key + ".md")
    doc = BeautifulSoup(MARKDOWN(source.read_text()), "html.parser")
    if doc.h1:
        doc.h1.decompose()
    if page.key == "workflow":
        insert_workflow_figures(doc, lang)
    for node in doc.select("a[href], img[src]"):
        attr = "href" if node.name == "a" else "src"
        link = urlsplit(node[attr])
        if not link.scheme and link.path.startswith("../../assets/"):
            node[attr] = relative(page.folder(lang), link.path[6:]) + ("#" + link.fragment if link.fragment else "")
    for a in doc.select("a[href]"):
        link = urlsplit(a["href"])
        if link.scheme or not link.path.endswith(".md"):
            continue
        target = BY_KEY[Path(link.path).stem]
        other = "zh" if link.path.startswith("../zh/") else lang
        a["href"] = page_link(target, other, page.folder(lang)) + ("#" + link.fragment if link.fragment else "")

    for image in doc.select("p > img:only-child"):
        caption = image.attrs.pop("title", "")
        figure = image.parent
        figure.name = "figure"
        figure["class"] = "article-figure"
        full = doc.new_tag("a", href=image["src"], target="_blank", rel="noopener")
        image.wrap(full)
        image["loading"] = "lazy"
        if caption:
            legend = doc.new_tag("figcaption")
            legend.string = caption
            editable = Path(image["src"]).name.replace("-" + lang + ".svg", ".drawio")
            if (ROOT / "assets/figures" / editable).is_file():
                editor_link = doc.new_tag("a", href=relative(page.folder(lang), "assets/figures/" + editable),
                                          download=editable)
                editor_link.string = "下载可编辑图" if lang == "zh" else "Download editable figure"
                legend.append(" · ")
                legend.append(editor_link)
            figure.append(legend)
        for node in figure.select("a[href], img[src]"):
            attr = "href" if node.name == "a" else "src"
            digest = figure_versions.get(Path(node[attr]).name)
            if digest:
                node[attr] += "?v=" + digest
        illustration = Path(urlsplit(image["src"]).path)
        if illustration.suffix == ".svg" and illustration.name in figure_versions:
            image.wrap(doc.new_tag("picture"))
            image.insert_before(doc.new_tag("source", media="(prefers-reduced-motion: reduce)",
                                            srcset=image["src"] + "#still"))
    for table in doc.select("table"):
        labels = [th.get_text(strip=True) for th in table.select("thead th")]
        for row in table.select("tbody tr"):
            for cell, label in zip(row.select("td"), labels):
                cell["data-label"] = label
    headings, entries, used = [], [], Counter()
    resource_sources = {}
    for node in doc.select("h2,h3,li"):
        title = node.get_text(" ", strip=True)
        heading = node.name.startswith("h")
        a = node.find("a")
        if not heading and not (page.key in CATALOG and a):
            continue
        name = title if heading else a.get_text(" ", strip=True)
        base = node.get("id") or slug(name)
        used[base] += 1
        anchor = base if used[base] == 1 else f"{base}-{used[base]}"
        node["id"] = anchor
        if heading:
            headings.append({"text": title, "id": anchor, "level": node.name})
        else:
            resource_sources[anchor] = a["href"]
            entry = {"label": name, "text": title, "anchor": anchor}
            if page.key == "papers":
                entry["paper_title"] = a.get("title", "")
                location = urlsplit(a["href"])
                if location.hostname == "arxiv.org" and location.path.startswith("/abs/"):
                    entry["identifier"] = "arXiv:" + location.path.removeprefix("/abs/")
            entries.append(entry)

    intro = DESCRIPTIONS.get(page.key)
    description = intro[LANGUAGES.index(lang)] if intro else ""
    intro_html = ""
    if not description and doc.find("p"):
        description = doc.p.get_text(" ", strip=True)
        if doc.find(["h2", "p"]) == doc.p:
            intro_html = doc.p.decode_contents()
            doc.p.decompose()
    search = list(entries)
    for h in doc.select("h2,h3"):
        chunks = []
        for sibling in h.next_siblings:
            if sibling.name in ("h2", "h3"):
                break
            if sibling.name and (page.key not in CATALOG or sibling.name != "ul"):
                chunks.append(sibling.get_text(" ", strip=True))
        search.append({"label": h.get_text(strip=True), "text": " ".join(chunks), "anchor": h["id"]})
    search.append({"label": page.title(lang), "text": description, "anchor": ""})
    count = sum(h["level"] == "h2" for h in headings) if page.key == "benchmarks" else len(entries)
    return dict(body=str(doc), headings=headings, count=count, description=description, intro_html=intro_html,
                search=search, resource_sources=resource_sources)


def site_update_date():
    inputs = ("content", "templates", "assets", "scripts", "requirements.txt")
    try:
        stamp = subprocess.check_output(
            ["git", "log", "--first-parent", "-1", "--format=%ct", "HEAD", "--", *inputs],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None  # A source archive can be built without Git history.
    if stamp:
        return datetime.fromtimestamp(int(stamp), timezone(timedelta(hours=8))).date()
    return None


def build():
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()[:10]

    figure_versions = {path.name: digest(path) for path in (ROOT / "assets/figures").iterdir() if path.is_file()}
    harbor_example = load_example(ROOT)
    content = {(l, p.key): read_page(p, l, figure_versions) for l in LANGUAGES for p in PAGES}
    navigation = [
        (group, [(label, list(items)) for label, items in groupby(members, attrgetter("subsection"))])
        for group, members in groupby(PAGES, attrgetter("group"))
    ]
    updated = site_update_date()
    repo = os.getenv("GITHUB_REPOSITORY", "")
    if repo and not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
        raise ValueError("Invalid GITHUB_REPOSITORY")
    repo_url = "https://github.com/" + repo if repo else ""
    public_url = os.getenv("SITE_URL", "").rstrip("/")
    OUT.mkdir(exist_ok=True)
    published_example = OUT / "assets/harbor"
    if published_example.is_dir():
        shutil.rmtree(published_example)
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    # Older builds copied the Markdown downloads here. Drop those generated files on rebuild.
    legacy_downloads = OUT / "source"
    if legacy_downloads.is_dir():
        shutil.rmtree(legacy_downloads)
    (OUT / ".nojekyll").touch()
    template = ENV.get_template("page.html")
    redirect_template = ENV.get_template("redirect.html")
    versions = {path.name: digest(path) for path in (ROOT / "assets").iterdir() if path.is_file()}
    for lang in LANGUAGES:
        index = []
        for page in PAGES:
            folder = page.folder(lang)
            for entry in content[lang, page.key]["search"]:
                index.append({**entry, "page": page.title(lang), "url": (folder + "/" if folder else "") +
                              ("#" + entry["anchor"] if entry["anchor"] else "")})
        # A script data block must never contain a literal HTML end tag.
        search_json = json.dumps(index, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
        (OUT / f"search-{lang}.json").write_text(search_json)
        for i, page in enumerate(PAGES):
            data = content[lang, page.key]
            folder = page.folder(lang)
            href = lambda key, language=lang: page_link(BY_KEY[key], language, folder)
            asset = lambda path: relative(folder, path)
            other = content["en" if lang == "zh" else "zh", page.key]
            other_ids = {entry["anchor"] for entry in other["search"] if entry["anchor"]}
            fragments = {entry["anchor"]: entry["anchor"] for entry in data["search"] if entry["anchor"] in other_ids}
            translated_sources = {source: anchor for anchor, source in other["resource_sources"].items()}
            for anchor, source in data["resource_sources"].items():
                if source in translated_sources:
                    fragments[anchor] = translated_sources[source]
            headings, translated = data["headings"], other["headings"]
            if [h["level"] for h in headings] == [h["level"] for h in translated]:
                fragments.update({a["id"]: b["id"] for a, b in zip(headings, translated)})
            html = template.render(harbor=harbor_example, versions=versions, brand=BY_KEY["home"].title(lang), fragments=fragments, search_json=search_json, page=page, lang=lang, zh=lang == "zh", navigation=navigation,
                                   previous=PAGES[i - 1] if i else None, upcoming=PAGES[i + 1] if i + 1 < len(PAGES) else None,
                                   href=href, asset=asset, repo=repo_url, public_url=public_url, folder=folder,
                                   root=relative(folder, ".") + "/", updated=updated,
                                   **data)
            target = OUT / folder / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html)

    def redirect(folder, page, lang, section=""):
        destination = page_link(page, lang, folder)
        canonical = public_url + "/" + (page.folder(lang) + "/" if page.folder(lang) else "") if public_url else destination
        output = OUT / folder / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(redirect_template.render(target=destination, section=section, canonical=canonical,
                                                    lang=lang, title=page.title(lang)))

    for page in PAGES:
        old_folder = posixpath.join("en", page.route).rstrip("/")
        redirect(old_folder, page, "en")
    for prefix, lang in (("", "en"), ("zh", "zh"), ("en", "en")):
        for topic in MERGED_DESIGN_TOPICS:
            redirect(posixpath.join(prefix, "design", topic), BY_KEY["design-review"], lang, topic)
    print(f"Built {len(PAGES) * len(LANGUAGES)} pages and {len(PAGES) + 3 * len(MERGED_DESIGN_TOPICS)} redirects in {OUT}")


if __name__ == "__main__":
    build()
