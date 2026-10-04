"""Snapshot selected licensed BO3 tutorials; never installs or edits game files.

Run from the repo root. Network access is needed only for collection;
--verify checks all stored sources and readable derivatives offline.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
REPO = "UGX-Mods/community-wiki"
COMMIT = "331184f27904c1fbe24cd59b5d752511f698746a"
BASE = "Modding/Black-Ops-3-Modtools/"
PAGES = [
    ("radiant-black", BASE + "Applications-and-Tools/Radiant-Black.html"),
    ("asset-property-editor", BASE + "Applications-and-Tools/Asset-Property-Editor.html"),
    ("zones", BASE + "Mapping/Adding-Zones.html"),
    ("zombie-spawners-risers-barriers", BASE + "Mapping/Adding-Zombie-Spawners-Risers-and-Window-Barriers.html"),
    ("mystery-box-locations", BASE + "Mapping/Adding-Pandoras-Box-locations.html"),
    ("dogs", BASE + "Mapping/Adding-Dog-Spawners-or-Disabling-Dog-Rounds.html"),
    ("script-error-information", BASE + "Script/How-to-display-more-script-error-information.html"),
    ("purchase-loops", BASE + "Script/Purchase-Loops.html"),
    ("weapon-system", BASE + "Script/Weapon-System.html"),
    ("weapon-list", BASE + "Script/Weapon-System/Weapon-List.html"),
    ("waw-scripting-differences", BASE + "Script/Whats-changed-from-WaW-scripting.html"),
    ("materials-and-textures", BASE + "Asset-Conversion/Adding-custom-materials-and-textures.html"),
    ("models", BASE + "Asset-Conversion/Adding-custom-models.html"),
    ("sounds", BASE + "Asset-Conversion/Adding-custom-sounds.html"),
    ("soundaliases", BASE + "Sounds/Creating-Modifying-Soundaliases-and-Converting-Sounds.html"),
]
VENDOR = ROOT / "tutorial-library" / "vendor" / "ugx"
MANIFEST = ROOT / "tutorial-library" / "sources.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class TutorialText(HTMLParser):
    """Preserve headings, table cells, code, links; omit scripts and comments."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
        self.pre = 0
        self.links = []
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self.parts.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in ("p", "div", "ul", "ol", "table", "tr") and not self.in_cell:
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag in ("td", "th"):
            self.in_cell = True
            self.parts.append(" | ")
        elif tag == "br":
            self.parts.append("\n")
        elif tag == "pre":
            self.pre += 1
            self.parts.append("\n\n```text\n")
        elif tag == "a":
            self.links.append(attrs.get("href", ""))
        elif tag == "img":
            self.parts.append(" [image reference: " + attrs.get("src", "") + "] ")
        elif tag == "iframe":
            self.parts.append(" [video reference: " + attrs.get("src", "") + "] ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "pre":
            self.pre = max(0, self.pre - 1)
            self.parts.append("\n```\n\n")
        elif tag == "a" and self.links:
            self.parts.append(" (" + self.links.pop() + ")")
        elif tag in ("td", "th"):
            self.in_cell = False
        elif tag in ("p", "h1", "h2", "h3", "h4", "tr", "li") and not self.in_cell:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data if self.pre else re.sub(r"\s+", " ", data))

    def result(self):
        content = "".join(self.parts)
        content = re.sub(r"[ \t]+\n", "\n", content)
        return re.sub(r"\n{3,}", "\n\n", content).strip() + "\n"


def fetch(path):
    url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{quote(path, safe='/')}"
    result = subprocess.run(
        ["curl.exe", "-sS", "-L", "--fail", "--max-time", "45", url],
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Download failed for {path}: {result.stderr.decode(errors='replace').strip()}")
    if not result.stdout:
        raise RuntimeError(f"Empty download for {path}")
    return url, result.stdout


def verify():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    problems = []
    for entry in manifest["files"]:
        for kind in ("source", "text"):
            if kind not in entry:
                continue
            item = entry[kind]
            path = ROOT / item["path"]
            if not path.is_file() or sha(path.read_bytes()) != item["sha256"]:
                problems.append(item["path"])
    if problems:
        raise SystemExit("Missing/modified snapshot files: " + ", ".join(problems))
    print(json.dumps({"verified_files": sum(1 + ("text" in e) for e in manifest["files"]),
                      "tutorials": len(PAGES), "commit": manifest["commit"], "errors": 0}))


def collect():
    if MANIFEST.exists():
        raise SystemExit("Snapshot already exists. Use --verify; review updates as a separate version.")
    license_url, license_data = fetch("LICENSE")
    if b"GNU AFFERO GENERAL PUBLIC LICENSE" not in license_data or b"Version 3" not in license_data:
        raise SystemExit("Unexpected upstream license; stopped before storing tutorial content.")
    requests = [("LICENSE", "LICENSE"), ("CREDITS", "CREDITS.md"), ("UPSTREAM_README", "README.md")] + PAGES
    # All requests complete successfully before creating the snapshot.
    with ThreadPoolExecutor(max_workers=4) as pool:
        downloaded = list(pool.map(lambda pair: (pair, fetch(pair[1])), requests))
    VENDOR.mkdir(parents=True, exist_ok=True)
    entries = []
    for (slug, upstream_path), (url, data) in downloaded:
        extension = ".html" if upstream_path.endswith(".html") else (".md" if upstream_path.endswith(".md") else "")
        target = VENDOR / (slug + extension)
        target.write_bytes(data)
        entry = {"id": slug, "upstream_path": upstream_path, "url": url,
                 "author_source_url": f"https://github.com/{REPO}/blob/{COMMIT}/{upstream_path}",
                 "license": "AGPL-3.0 (see unchanged LICENSE and upstream notices)",
                 "source": {"path": target.relative_to(ROOT).as_posix(), "sha256": sha(data), "bytes": len(data)}}
        if extension == ".html":
            parser = TutorialText()
            parser.feed(data.decode("utf-8"))
            text_path = VENDOR / (slug + ".txt")
            text_data = (
                "UGX-Mods community wiki — readable text derivative\n"
                f"Original: {entry['author_source_url']}\n"
                f"Snapshot commit: {COMMIT}\n"
                "License: AGPL-3.0; upstream notices retained in source HTML.\n"
                "Local change: HTML converted to plain text; media and relative links are references only.\n"
                "This derivative shares the upstream license. Original HTML is authoritative.\n\n"
                + parser.result()
            ).encode("utf-8")
            text_path.write_bytes(text_data)
            entry["text"] = {"path": text_path.relative_to(ROOT).as_posix(), "sha256": sha(text_data), "bytes": len(text_data)}
        entries.append(entry)
    MANIFEST.write_bytes((json.dumps({
        "schema_version": 1, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": f"https://github.com/{REPO}", "commit": COMMIT,
        "selection": "BO3-only tutorial pages plus upstream license, credits and README; no game files or image/video downloads",
        "notes": "Pinned upstream repository is a Confluence migration; old links/media may be unavailable. Tutorials are not local runtime validation.",
        "files": entries,
    }, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    verify()


def refresh_text():
    """Rebuild readable derivatives offline while preserving upstream bytes."""
    verify()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        if "text" not in entry:
            continue
        text_path = ROOT / entry["text"]["path"]
        header = text_path.read_text(encoding="utf-8").split("\n\n", 1)[0]
        parser = TutorialText()
        parser.feed((ROOT / entry["source"]["path"]).read_text(encoding="utf-8"))
        text_data = (header + "\n\n" + parser.result()).encode("utf-8")
        text_path.write_bytes(text_data)
        entry["text"].update(sha256=sha(text_data), bytes=len(text_data))
    manifest["text_refreshed_at_utc"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_bytes((json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    verify()


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    action = args.add_mutually_exclusive_group()
    action.add_argument("--verify", action="store_true")
    action.add_argument("--refresh-text", action="store_true")
    options = args.parse_args()
    if options.verify:
        verify()
    elif options.refresh_text:
        refresh_text()
    else:
        collect()
