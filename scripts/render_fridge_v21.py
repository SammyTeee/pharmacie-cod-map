"""Render the saved v21 fridge with reduced review exposure; do not resave map."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-shopfronts-fridge-v21.blend'
scene=bpy.data.scenes['01 Ground floor - mapped rooms'];bpy.context.window.scene=scene
scene.camera=bpy.data.objects['Review v21 | fridge against bar']
dest=ROOT/'recon/v21'
scene.view_settings.exposure=-1.5
source=(ROOT/'scripts/update_fridge_v21.py').read_text().split('# Temporary render lighting is deliberately not saved into the map.')[1]
exec(source.split('print(json.dumps(report))')[0])
