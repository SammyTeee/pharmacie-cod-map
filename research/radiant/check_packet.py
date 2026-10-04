"""Check offline tutorial integrity and planning-document consistency only."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

from collect_tutorials import verify

REPO = Path(__file__).resolve().parents[2]
ROOT = Path(__file__).resolve().parent
DOCUMENTS = [
    ROOT / "README.md",
    ROOT / "tutorial-library/README.md",
    ROOT / "tutorial-library/EXTERNAL_READING_NOTES.md",
    REPO / "docs/RADIANT_CONVERSION_PLAYBOOK.md",
    REPO / "docs/RADIANT_STOCK_GAMEPLAY_AUDIT.md",
    REPO / "docs/RADIANT_GAMEPLAY_PLACEMENT_PLAN.md",
    REPO / "docs/ZOMBIES_DESIGN_V29.md",
]


def main():
    verify()
    registry_path = REPO / "docs/radiant-gameplay-plan.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entries = [entry for name in ("zones", "gates", "player_starts", "risers", "items", "future")
               for entry in registry[name]]
    ids = [entry["id"] for entry in entries]
    problems = []
    if len(ids) != len(set(ids)):
        problems.append("Duplicate planning IDs")
    zone_ids = {entry["id"] for entry in entries if entry["id"].startswith("Z") and "_" not in entry["id"]}
    for entry in entries:
        for field in ("zone", "from_zone", "to_zone"):
            if field in entry and entry[field] not in zone_ids:
                problems.append(f"{entry['id']}: unknown {field} {entry[field]}")
        for field in ("origin_m", "angles_deg"):
            if field in entry and (len(entry[field]) != 3 or not all(isinstance(v, (int, float)) for v in entry[field])):
                problems.append(f"{entry['id']}: invalid {field}")
        for field in ("bounds_m", "collision_bounds_m", "use_bounds_m"):
            for bounds in entry.get(field, []):
                if len(bounds) != 6 or any(bounds[i] >= bounds[i + 1] for i in (0, 2, 4)):
                    problems.append(f"{entry['id']}: invalid {field}")
    if len(registry["player_starts"]) != 4 or len(registry["risers"]) != 11:
        problems.append("Unexpected baseline start/riser count")
    if sum(entry["cost"] for entry in registry["gates"]) != 3000:
        problems.append("Baseline gate costs no longer match documented total")
    for entry in registry["future"]:
        if entry["id"] in ("G04", "G05") and entry.get("cost") is not None:
            problems.append(f"{entry['id']}: future gate price invented before balance review")

    local_link_count = 0
    for document in DOCUMENTS:
        content = document.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            target = target.strip("<>").split("#", 1)[0]
            if not target or re.match(r"[a-z]+://", target):
                continue
            local_link_count += 1
            if not (document.parent / unquote(target)).exists():
                problems.append(f"Missing link in {document.relative_to(REPO)}: {target}")

    cases_path = ROOT / "manual-test-record.csv"
    with cases_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        cases = list(reader)
        for case in cases:
            if None in case or any(value is None for value in case.values()):
                problems.append(f"CSV field count mismatch: {case.get('case_id')}")
        if len({case["case_id"] for case in cases}) != len(cases):
            problems.append("Duplicate manual test IDs")

    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Offline documentation/source consistency, not engine/editor/runtime tests",
        "registry_ids": len(ids), "player_starts": len(registry["player_starts"]),
        "baseline_risers": len(registry["risers"]), "local_links": local_link_count,
        "manual_cases": len(cases), "errors": problems,
        "documents": [{"path": path.relative_to(REPO).as_posix(),
                       "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                      for path in DOCUMENTS + [registry_path, cases_path]],
    }
    if problems:
        raise SystemExit("\n".join(problems))
    (ROOT / "packet-validation.json").write_bytes((json.dumps(report, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({key: value for key, value in report.items() if key != "documents"}))


if __name__ == "__main__":
    main()
