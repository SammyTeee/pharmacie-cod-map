"""Reproduce v25 route calibration without modifying the Blender checkpoint.

This is chainage calibration, not a geographic affine transform. In particular,
it must never be used to place Holmdale by extrapolating the old capture walk.
"""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]


def audit():
    files = {
        "centreline": ROOT / "recon/v22/validation.json",
        "taraj": ROOT / "recon/v24/validation.json",
        "walk": ROOT / "references/streetview-capture/taraj-to-pharmacie/walk-state.json",
    }
    data = {k: json.loads(p.read_text()) for k, p in files.items()}
    path = data["centreline"]["melton_centreline"]
    chainages = [0.0]
    for a, b in zip(path, path[1:]):
        chainages.append(chainages[-1] + math.dist(a, b))
    pivot = data["taraj"]["road_pivot"]
    candidates = []
    for i, (a, b) in enumerate(zip(path, path[1:])):
        length = math.dist(a, b)
        u = [(b[j] - a[j]) / length for j in range(2)]
        t = max(0, min(length, sum((pivot[j] - a[j]) * u[j] for j in range(2))))
        p = [a[j] + t * u[j] for j in range(2)]
        candidates.append((math.dist(pivot, p), chainages[i] + t, p))
    error, taraj_s, projected = min(candidates)
    stops = data["walk"]["completed_stops"]
    distances = [0.0]
    for a, b in zip(stops, stops[1:]):
        dx = (b["longitude"] - a["longitude"]) * 111320 * math.cos(math.radians(a["latitude"]))
        dy = (b["latitude"] - a["latitude"]) * 111320
        distances.append(distances[-1] + math.hypot(dx, dy))
    scale = (taraj_s - 18) / distances[-1]
    assert scale > 0 and error < .01
    return {
        "method": "Exact scalar-chainage formula from scripts/model_syston_v25.py, double precision",
        "source_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()},
        "blender_centreline": path,
        "blender_centreline_length": chainages[-1],
        "taraj_chainage": taraj_s,
        "taraj_projected_pivot": projected,
        "taraj_projection_error": error,
        "captured_walk_metres_estimate": distances[-1],
        "blender_units_per_capture_metre_estimate": scale,
        "stop_chainages": [{"stop": s["stop"], "latitude": s["latitude"], "longitude": s["longitude"], "chainage": taraj_s - d * scale} for s, d in zip(stops, distances)],
        "extension_seam": {"position": path[-1], "tangent": [(path[-1][j]-path[-2][j])/math.dist(path[-1],path[-2]) for j in range(2)]},
        "limits": ["Existing walk covers Taraj to town centre only.", "No new route has been traced or georeferenced.", "Scale is a gameplay estimate, not surveyed metres.", "House pin and panorama camera differ and must not be treated as the same point.", "No house footprint or architecture inferred from address."],
        "house_user_supplied_place_lat_lon": [52.693457, -1.0800171],
        "house_user_supplied_camera_lat_lon": [52.6933309, -1.0789429],
        "blender_modified": False,
        "bo3_verified": False,
    }


if __name__ == "__main__":
    report = audit()
    out = ROOT / "recon/v41/frame-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("taraj_chainage", "blender_centreline_length", "captured_walk_metres_estimate", "blender_units_per_capture_metre_estimate", "extension_seam")}, indent=2))
