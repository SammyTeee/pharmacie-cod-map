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
    "z_max": 256,
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
    r = ROOM
    x0, x1 = r["x_min"], r["x_max"]
    y0, y1 = r["y_min"], r["y_max"]
    z0, z1 = r["z_min"], r["z_max"]
    w, slab = r["wall"], r["slab"]
    mat = "t7_concrete_trowelled"  # Seen on BO3 stock zm_giant brush faces.

    boxes: list[tuple[str, tuple[int, int, int, int, int, int]]] = [
        ("floor", (x0 - w, x1 + w, y0 - w, y1 + w, z0 - slab, z0)),
        ("ceiling", (x0 - w, x1 + w, y0 - w, y1 + w, z1, z1 + slab)),
        ("west wall south", (x0 - w, x0, y0 - w, 432, z0, z1)),
        ("west wall north", (x0 - w, x0, 544, y1 + w, z0, z1)),
        ("west wall door lintel", (x0 - w, x0, 432, 544, 208, z1)),
        ("east wall", (x1, x1 + w, y0 - w, y1 + w, z0, z1)),
        # Front entrance: a 192-unit door opening in the street-end wall.
        ("street wall west", (x0, -96, y0 - w, y0, z0, z1)),
        ("street wall east", (96, x1, y0 - w, y0, z0, z1)),
        ("street wall lintel", (-96, 96, y0 - w, y0, 224, z1)),
        ("bar end wall", (x0, x1, y1, y1 + w, z0, z1)),
        # Toilet room beside the bar. The east partition has a proper doorway.
        ("toilet west partition", (-288, -272, 192, 512, z0, 224)),
        ("toilet north partition", (-272, -64, 496, 512, z0, 224)),
        ("toilet south partition", (-272, -64, 192, 208, z0, 224)),
        ("toilet east north", (-80, -64, 192, 272, z0, 224)),
        ("toilet east south", (-80, -64, 352, 512, z0, 224)),
        ("toilet east lintel", (-80, -64, 272, 352, 208, 224)),
        # Small covered outside smoking area on the west side, with a doorway
        # from the pub and an open doorway facing the surrounding sky shell.
        ("smoking floor", (-672, -352, 368, 736, z0 - slab, z0)),
        ("smoking ceiling", (-672, -352, 368, 736, z1, z1 + slab)),
        ("smoking west wall north", (-672, -656, 560, 736, z0, z1)),
        ("smoking west wall south", (-672, -656, 368, 432, z0, z1)),
        ("smoking south wall", (-672, -352, 368, 384, z0, z1)),
        ("smoking north wall", (-672, -352, 720, 736, z0, z1)),
        ("smoking pub wall south", (-368, -352, 368, 432, z0, z1)),
        ("smoking pub wall north", (-368, -352, 544, 736, z0, z1)),
        ("smoking pub door lintel", (-368, -352, 432, 544, 208, z1)),
        # Stair passage on the east. Treads ascend toward the rear landing;
        # the open side remains connected to the main room for the blockout.
        ("stair west partition", (64, 80, 144, 560, z0, 208)),
        ("stair east partition south", (272, 288, 144, 480, z0, 208)),
        ("stair east partition north", (272, 288, 544, 560, z0, 208)),
        ("upper landing", (80, 272, 480, 560, 96, 112)),
        # Raised table platform and simple table placeholders in the main hall.
        ("raised table platform", (16, 304, -144, 176, 0, 12)),
        ("platform step one", (16, 304, -192, -144, 0, 4)),
        ("platform step two", (16, 304, -176, -144, 4, 8)),
        ("table 1", (-256, -160, -448, -352, 0, 32)),
        ("table 2", (144, 224, -384, -288, 0, 32)),
        ("table 3", (-256, -160, -128, -32, 0, 32)),
        ("table 4", (176, 256, 224, 304, 0, 32)),
        # Plain blockout bar and backbar at the north end.
        ("bar counter", (-176, 176, 624, 688, 0, 40)),
        ("bar top", (-192, 192, 616, 696, 40, 52)),
        ("backbar", (-224, 224, 736, 768, 52, 184)),
    ]
    # Eight solid risers give the upstairs stair passage an immediately
    # legible, walkable first-pass shape.
    for index in range(8):
        y = 160 + index * 40
        height = 12 + (index + 1) * 12
        boxes.append((f"stair tread {index + 1}", (96, 256, y, y + 40, 0, height)))
    result = []
    for offset, (_label, bounds) in enumerate(boxes):
        result.append(box_brush(first_number + offset, bounds, mat, nl))
    return "".join(result)


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
        -672, ROOM["x_max"],
        ROOM["y_min"], ROOM["y_max"],
        ROOM["z_min"], ROOM["z_max"],
    )
    return brush_re.sub(volume_brush(0, bounds, nl), inner, count=1)


ORIGINS_BY_MODEL = {
    "barricade_reciever_wood.map": "320 -32 0",
    "power_switch.map": "288 96 0",
    "buyable_magic_box_start.map": "-240 552 0",
    "vending_revive_struct.map": "240 552 0",
    "vending_juggernaut_struct.map": "-240 432 0",
    "vending_sleight_struct.map": "240 432 0",
    "vending_doubletap_struct.map": "-240 280 0",
    "vending_weapon_upgrade_spawnable.map": "240 280 0",
    "spawnable_weapon_shotgun_pump.map": "-280 -32 0",
}


def update_entity(block: str, nl: str) -> str:
    classname = kv(block, "classname") or ""
    model = kv(block, "model") or ""
    noteworthy = kv(block, "script_noteworthy") or ""
    targetname = kv(block, "targetname") or ""
    origin = None

    for suffix, location in ORIGINS_BY_MODEL.items():
        if model.endswith(suffix):
            origin = location
            break

    if classname == "actor_zm_factory_zombie":
        origin = "0 552 28"
    elif classname == "script_struct" and noteworthy == "riser_location":
        old_origin = kv(block, "origin")
        if old_origin == "576 192 0":
            origin = "280 192 0"
        elif old_origin == "-576 192 0":
            origin = "-280 192 0"
        elif old_origin == "0 576 0":
            origin = "0 704 0"
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
