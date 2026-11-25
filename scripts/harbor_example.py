"""Collect the published Harbor files for the static file browser."""
import hashlib
import json
from urllib.parse import quote
from zipfile import ZipFile


def file_size(size):
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size / (1024 * 1024):.1f} MiB"


def preview_kind(path):
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        return "image"
    if path.stat().st_size > 4 * 1024 * 1024:
        return "large"
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "binary"
    return "binary" if "\0" in text else "text"


def load_example(root):
    base = root / "assets" / "harbor"
    meta = json.loads((base / "example.json").read_text(encoding="utf-8"))
    directory = base / meta["slug"]
    archive = base / meta["archive"]
    files = {}
    edition = hashlib.sha256(archive.read_bytes()).hexdigest()[:12]

    def download_url(path):
        return quote(path.relative_to(root).as_posix()) + "?v=" + edition

    def visit(path):
        children = []
        for entry in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold())):
            if entry.is_dir():
                branch, count = visit(entry)
                children.append({"name": entry.name, "children": branch, "count": count})
            else:
                key = entry.relative_to(directory).as_posix()
                item = {"name": entry.name, "path": key, "url": download_url(entry),
                        "size": file_size(entry.stat().st_size), "kind": preview_kind(entry)}
                files[key] = item
                children.append(item)
        return children, sum(child.get("count", 1) for child in children)

    tree, count = visit(directory)
    # Each download must contain the same files and bytes as the online reader.
    with ZipFile(archive) as package:
        members = {f"{directory.name}/{path}": directory / path for path in files}
        entries = [item.filename for item in package.infolist() if not item.is_dir()]
        if sorted(entries) != sorted(members):
            raise ValueError(f"{archive.name}: file list differs from the reader")
        for name, source in members.items():
            if package.read(name) != source.read_bytes():
                raise ValueError(f"{archive.name}: {name} differs from the reader")

    return {
        **meta, "tree": tree, "count": count,
        "instruction": files["instruction.md"], "readme": files["README.md"],
        "instruction_text": (directory / "instruction.md").read_text(encoding="utf-8"),
        "archive_size": file_size(archive.stat().st_size), "archive_url": download_url(archive),
        "directory_url": quote(directory.relative_to(root).as_posix()),
    }
