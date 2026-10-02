"""Generate the first compact, code-authored BO3 Zombies room from our template."""

from __future__ import annotations

import re
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "map_source" / "zm" / "zm_pharmacie.template.map"
OUTPUT = ROOT / "map_source" / "zm" / "zm_pharmacie.map"
GUID_NAMESPACE = uuid.UUID("b1643616-c131-4516-b8c2-7e3559725262")

# BO3 map units are treated as inches. The pub room runs along +Y, matching the
# template's front player spawn at negative Y and zombie spawner at positive Y.
ROOM = {
    "x_min": -352,
    "x_max": 352,
    "y_min": -640,
    "y_max": 800,
    "z_min": 0,
    "z_max": 320,
    "wall": 16,
    "slab": 16,
}


def line_ending(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def fmt(n: int | float) -> str:
    return str(int(n)) if int(n) == n else f"{n:g}"


def box_brush(number: int, bounds: tuple[int, int, int, int, int, int], material: str, nl: str) -> str:
    """Make one axis-aligned brush using inward-pointing plane normals."""
    x0, x1, y0, y1, z0, z1 = bounds
    if x0 >= x1 or y0 >= y1 or z0 >= z1:
        raise ValueError(f"invalid brush bounds: {bounds}")

    faces = [
        # bottom, top, south, north, west, east
        ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0)),
        ((x0, y0, z1), (x0, y1, z1), (x1, y1, z1)),
        ((x0, y0, z0), (x0, y0, z1), (x1, y0, z1)),
        ((x0, y1, z0), (x1, y1, z0), (x1, y1, z1)),
        ((x0, y0, z0), (x0, y1, z0), (x0, y1, z1)),
        ((x1, y0, z0), (x1, y0, z1), (x1, y1, z1)),
    ]
    guid = uuid.uuid5(GUID_NAMESPACE, f"zm_pharmacie:brush:{number}:{bounds}:{material}")
    rows = [f"// brush {number}", "{", f' guid "{{{guid}}}"']
    for a, b, c in faces:
        points = " ".join(f"( {fmt(x)} {fmt(y)} {fmt(z)} )" for x, y, z in (a, b, c))
        rows.append(
            f" {points} {material} 128 128 0 0 0 0 lightmap_gray 16384 16384 0 0 0 0"
        )
    rows.append("}")
    return nl.join(rows) + nl


def volume_brush(number: int, bounds: tuple[int, int, int, int, int, int], nl: str) -> str:
    x0, x1, y0, y1, z0, z1 = bounds
    faces = [
        ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0)),
        ((x0, y0, z1), (x0, y1, z1), (x1, y1, z1)),
        ((x0, y0, z0), (x0, y0, z1), (x1, y0, z1)),
        ((x0, y1, z0), (x1, y1, z0), (x1, y1, z1)),
        ((x0, y0, z0), (x0, y1, z0), (x0, y1, z1)),
        ((x1, y0, z0), (x1, y0, z1), (x1, y1, z1)),
    ]
    guid = uuid.uuid5(GUID_NAMESPACE, f"zm_pharmacie:volume:{number}:{bounds}")
    rows = [f"// brush {number}", "{", f' guid "{{{guid}}}"']
    for a, b, c in faces:
        points = " ".join(f"( {fmt(x)} {fmt(y)} {fmt(z)} )" for x, y, z in (a, b, c))
        rows.append(f" {points} volume 64 64 0 0 0 0 lightmap_gray 16384 16384 0 0 0 0")
    rows.append("}")
    return nl.join(rows) + nl


def generated_room_brushes(first_number: int, nl: str) -> str:
    from svg_blockout import boxes
    from photo_panels import panels
    geometry = boxes()
    return (''.join(box_brush(first_number+i, bounds, blockout_material(label), nl)
                   for i, (label, bounds) in enumerate(geometry))
            + panels(first_number+len(geometry), nl))


def blockout_material(label: str) -> str:
    """Stock materials observed in the installed zm_giant source maps."""
    if label in {'main floor', 'vestibule floor', 'platform', 'bar', 'bar countertop',
                 'sofa', 'chairs', 'east landing', 'added-murb8s0z'} or label.startswith(
                     ('table', 'added-murb8s0z', 'rear stair ', 'east stair ', 'upstairs floor ')):
        return 't7_wood_planks_damaged_teak'
    if label.startswith(('patio ', 'forecourt ')) and not label.endswith('floor'):
        return 't7_brick_worn_heavy_grout_red'
    return 't7_concrete_trowelled'


def parse_entity_blocks(text: str) -> list[tuple[int, int, str]]:
    markers = list(re.finditer(r"(?m)^// entity \d+\r?$", text))
    found = []
    for marker in markers:
        opening = text.find("{", marker.end())
        if opening < 0:
            raise ValueError("entity marker has no opening brace")
        depth = 0
        closing = -1
        for i in range(opening, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    closing = i + 1
                    break
        if closing < 0:
            raise ValueError("unterminated entity block")
        found.append((marker.start(), closing, text[marker.start():closing]))
    if not found or '"classname" "worldspawn"' not in found[0][2]:
        raise ValueError("expected worldspawn as entity 0")
    return found


def kv(block: str, key: str) -> str | None:
    match = re.search(rf'(?m)^\s*"{re.escape(key)}"\s+"([^"]*)"', block)
    return match.group(1) if match else None


def add_room_to_worldspawn(block: str, nl: str) -> str:
    open_at = block.find("{")
    close_at = block.rfind("}")
    inner = block[open_at + 1:close_at]
    brush_re = re.compile(r"(?ms)^// brush (\d+)\r?\n\{.*?^\}\r?\n?")
    brushes = list(brush_re.finditer(inner))
    if not brushes:
        raise ValueError("template worldspawn has no brush children")
    prefix = inner[:brushes[0].start()]

    # Preserve only the enclosing sky shell. Replace the template tutorial
    # walls/floor with our room, leaving all non-worldspawn entities intact.
    sky = [m.group(0) for m in brushes if re.search(r"\)\s+sky\s", m.group(0))]
    sky_numbers = [int(m.group(1)) for m in brushes if re.search(r"\)\s+sky\s", m.group(0))]
    if len(sky) != 6:
        raise ValueError(f"expected six sky-shell brushes, found {len(sky)}")
    first_number = max(sky_numbers) + 1
    new_inner = prefix + "".join(sky)
    if new_inner and not new_inner.endswith(("\n", "\r")):
        new_inner += nl
    new_inner += generated_room_brushes(first_number, nl)
    return block[:open_at + 1] + new_inner + block[close_at:]


def patch_info_volume(block: str, nl: str) -> str:
    inner = block
    brush_re = re.compile(r"(?ms)^// brush (\d+)\r?\n\{.*?^\}\r?\n?")
    if not brush_re.search(inner):
        raise ValueError("start_zone info_volume is missing its brush")
    bounds = (
        -496, ROOM["x_max"],
        -1008, 1152,
        ROOM["z_min"], 640,
    )
    return brush_re.sub(volume_brush(0, bounds, nl), inner, count=1)


ORIGINS_BY_MODEL = {
    "barricade_reciever_wood.map": "320 192 0",
    "power_switch.map": "320 256 0",
    "buyable_magic_box_start.map": "-280 160 0",
    "vending_revive_struct.map": "-272 -576 0",
    "vending_juggernaut_struct.map": "-384 1072 0",
    "vending_sleight_struct.map": "-256 1072 0",
    "vending_doubletap_struct.map": "-128 272 0",
    "vending_weapon_upgrade_spawnable.map": "64 272 0",
    "spawnable_weapon_shotgun_pump.map": "-328 -480 0",
}


def update_entity(block: str, nl: str) -> str:
    classname = kv(block, "classname") or ""
    model = kv(block, "model") or ""
    noteworthy = kv(block, "script_noteworthy") or ""
    targetname = kv(block, "targetname") or ""
    origin = None

    # This layout uses floor risers, not the tutorial's freestanding window.
    if model.endswith('barricade_reciever_wood.map'):
        return ''
    if noteworthy == 'riser_location':
        block = block.replace('"receiver_set_entry_a"', '"find_flesh"')

    for suffix, location in ORIGINS_BY_MODEL.items():
        if model.endswith(suffix):
            origin = location
            break

    if classname == "actor_spawner_zm_factory_zombie":
        origin = "-280 640 8"
    elif noteworthy == "initial_spawn":
        old = (kv(block, "origin") or '').split()
        origin = f"{int(float(old[0])) // 3} {old[1]} 28"
    elif classname == "script_struct" and noteworthy == "riser_location":
        old_origin = kv(block, "origin")
        if old_origin == "576 192 0":
            origin = "288 160 0"
        elif old_origin == "-576 192 0":
            origin = "-280 320 0"
        elif old_origin == "0 576 0":
            origin = "-280 960 0"
    elif classname == "script_struct" and targetname == "intermission_b":
        origin = "280 -32 104"

    if origin:
        block, count = re.subn(
            r'(?m)^([ \t]*"origin"\s+")[^"]*(")',
            rf"\g<1>{origin}\g<2>",
            block,
            count=1,
        )
        if count != 1:
            raise ValueError(f"wanted to move {classname} ({model}) but it has no origin")

    if classname == "info_volume" and kv(block, "script_noteworthy") == "player_volume":
        block = patch_info_volume(block, nl)
    return block


def generate(text: str) -> str:
    nl = line_ending(text)
    entities = parse_entity_blocks(text)
    pieces = []
    cursor = 0
    for index, (start, end, block) in enumerate(entities):
        pieces.append(text[cursor:start])
        if index == 0:
            block = add_room_to_worldspawn(block, nl)
        else:
            block = update_entity(block, nl)
        pieces.append(block)
        cursor = end
    pieces.append(text[cursor:])
    for i, y in enumerate((-480, -64, 320, 704, 1000)):
        pieces.append(nl + '// entity ' + str(100+i) + nl + '{' + nl +
                      f'"classname" "light"{nl}"origin" "0 {y} 220"{nl}' +
                      f'"_color" "1 0.88 0.7"{nl}"light" "450"{nl}' + '}' + nl)
    for i, y in enumerate((-480, -64, 320, 704)):
        pieces.append(nl + '// entity ' + str(110+i) + nl + '{' + nl +
                      f'"classname" "light"{nl}"origin" "0 {y} 548"{nl}' +
                      f'"_color" "1 0.88 0.7"{nl}"light" "450"{nl}' + '}' + nl)
    return "".join(pieces)


def main() -> None:
    if not TEMPLATE.exists():
        raise SystemExit(f"Missing generated template: {TEMPLATE}")
    source = TEMPLATE.read_bytes().decode("utf-8")
    output = generate(source)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(output.encode("utf-8"))
    print(f"Generated {OUTPUT.relative_to(ROOT)} from {TEMPLATE.relative_to(ROOT)}")
    print(f"Interior: {ROOM['x_max'] - ROOM['x_min']} x {ROOM['y_max'] - ROOM['y_min']} x {ROOM['z_max'] - ROOM['z_min']} units")
    print("Retained template gameplay entities, stock sky shell, and scripts; rebuilt world geometry.")


if __name__ == "__main__":
    main()
