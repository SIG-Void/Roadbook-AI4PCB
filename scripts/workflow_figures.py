"""Place credited KiCad illustrations beside the matching passages of the original notes."""
import json
from pathlib import Path

GUIDE = "https://docs.kicad.org/9.0/en/getting_started_in_kicad/getting_started_in_kicad.html"
LICENSE = "https://creativecommons.org/licenses/by/3.0/"
FIGURES = Path(__file__).resolve().parents[1] / "content/workflow-figures.json"


def insert_workflow_figures(doc, lang):
    for section in json.loads(FIGURES.read_text(encoding="utf-8")):
        title = section["heading"][lang]
        heading = doc.find(["h2", "h3"], string=title)
        if heading is None:
            raise ValueError(f"Missing workflow illustration heading: {title}")
        paragraphs = []
        for sibling in heading.next_siblings:
            if sibling.name in ("h2", "h3"):
                break
            if sibling.name == "p":
                paragraphs.append(sibling)
        position = section.get("after_paragraph", {}).get(lang, len(paragraphs))
        if not 1 <= position <= len(paragraphs):
            raise ValueError(f"Missing workflow illustration paragraph under {title}")

        gallery = doc.new_tag("div")
        gallery["class"] = "workflow-gallery"
        if len(section["images"]) == 2:
            gallery["class"] += " workflow-pair"
        for item in section["images"]:
            url = "../../assets/guide/kicad/" + item["file"]
            figure = doc.new_tag("figure")
            full = doc.new_tag("a", href=url, target="_blank", rel="noopener")
            full.append(doc.new_tag("img", src=url, alt=item["alt"][lang], loading="lazy",
                                    width=item["width"], height=item["height"]))
            figure.append(full)
            caption = doc.new_tag("figcaption")
            caption.string = item["caption"][lang]
            figure.append(caption)
            gallery.append(figure)

        credit = doc.new_tag("small", attrs={"class": "workflow-credit"})
        source = doc.new_tag("a", href=f'{GUIDE}#{section["source_section"]}')
        source.string = "KiCad Documentation Contributors"
        license_link = doc.new_tag("a", href=LICENSE)
        license_link.string = "CC BY 3.0"
        credit.extend(["© ", source, " · ", license_link])
        gallery.append(credit)
        paragraphs[position - 1].insert_after(gallery)
