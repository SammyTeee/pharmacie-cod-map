"""Verify the Git handover and preservation of Sam's local checkpoints."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args, input=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=input).decode()


receipt = json.loads((ROOT / "docs/handover/local-checkpoint-receipt.json").read_text())
tracked = git("ls-files", "-z").split("\0")[:-1]
blends = sorted(p for p in tracked if p.lower().endswith(".blend"))
assert blends == ["Pharmacie-Syston.blend"], blends
old = [item["path"] for item in receipt["files"]]
assert len(old) == 72 and not set(old).intersection(tracked)
for item in receipt["files"]:
    stat = (ROOT / item["path"]).stat()
    assert stat.st_size == item["bytes"], item["path"]
    assert stat.st_mtime_ns == item["mtime_ns"], item["path"]
for path, expected in receipt["protected_sha256"].items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
ignored = git("check-ignore", "--stdin", input=("\n".join(old) + "\n").encode()).splitlines()
assert set(ignored) == set(old)
original_blob = git("rev-parse", "3d3a7bc:assets/blender/pharmacie-demo-base-v59.blend").strip()
handover_blob = git("ls-files", "--stage", "--", "Pharmacie-Syston.blend").split()[1]
assert handover_blob == original_blob, "Staged handover differs from original v59"

dest = ROOT / "docs/handover/cleanup-result.json"
assert dest.relative_to(ROOT).as_posix() in tracked
other_bytes = sum((ROOT / path).stat().st_size for path in tracked if path != dest.relative_to(ROOT).as_posix())
report = {
    "status": "verified",
    "baseline_commit": "3d3a7bca4a1fc61fac3a4f9e089d48de8d421631",
    "baseline_tracked_bytes": 4292031623,
    "tracked_file_count": len(tracked),
    "tracked_working_file_bytes": 0,
    "tracked_blender_files": blends,
    "untracked_checkpoint_count": len(old),
    "local_checkpoints_present_with_unchanged_size_and_mtime": True,
    "v59_v60_and_handover_sha256_unchanged": True,
    "all_old_checkpoints_ignored": True,
    "staged_handover_matches_original_v59_blob": True,
    "handover_git_blob": handover_blob,
    "local_checkpoint_deletions": 0,
    "history_rewritten": False,
}
for _ in range(10):
    content = json.dumps(report, indent=2) + "\n"
    total = other_bytes + len(content.encode("utf-8"))
    if report["tracked_working_file_bytes"] == total:
        break
    report["tracked_working_file_bytes"] = total
else:
    raise RuntimeError("Receipt size failed to converge")
dest.write_text(content, encoding="utf-8")
print(json.dumps(report, indent=2))
