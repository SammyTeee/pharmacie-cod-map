"""Inspect the loaded handover without changing or saving any Blender data."""
import hashlib
import json
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[1]
source = Path(bpy.data.filepath)
images = []
for image in bpy.data.images:
    if image.source not in {"FILE", "TILED", "SEQUENCE", "MOVIE"}:
        continue
    packed = bool(image.packed_file or len(image.packed_files))
    resolved = bpy.path.abspath(image.filepath, library=image.library)
    images.append({"name": image.name, "source": image.source,
                   "path": image.filepath, "packed": packed,
                   "available": packed or Path(resolved).is_file()})

external = sorted(set(bpy.utils.blend_paths(absolute=True, packed=False)))
report = {
    "file": source.name,
    "bytes": source.stat().st_size,
    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "blender_version": bpy.app.version_string,
    "scenes": [{"name": scene.name, "objects": len(scene.objects)}
               for scene in bpy.data.scenes],
    "objects": len(bpy.data.objects),
    "meshes": len(bpy.data.meshes),
    "materials": len(bpy.data.materials),
    "images": images,
    "linked_libraries": [library.filepath for library in bpy.data.libraries],
    "unpacked_external_paths": external,
    "missing_images": [image["name"] for image in images if not image["available"]],
}
dest = ROOT / "docs" / "handover" / "blender-dependencies.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("HANDOVER_DEPENDENCIES", json.dumps(report), flush=True)
assert not report["missing_images"], "Missing image dependencies"
assert not report["linked_libraries"], "Linked libraries need separate packaging"
assert not external, "External dependencies need separate packaging"
