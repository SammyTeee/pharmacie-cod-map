"""Run in Blender: compare the pub's visible floors with static engine support.

Does not save or modify the scene. Stairwell openings are sampled only where
the evaluated visible floor exists. Walls/closed rooms do not imply access.
"""
from pathlib import Path
import sys
import json
import math
import hashlib
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from audit_bo3_core_ground import load_solids, support, world, UNIT
from audit_bo3_core_routes import vertices

scene = bpy.data.scenes['03 Both floors - assembled exterior']
bpy.context.window.scene = scene
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
map_path = ROOT/'map_source/zm/zm_pharmacie_core65.map'
solids = load_solids(map_path.read_text())
limits = [vertices(planes) for _,planes in solids]
lows = np.array([v.min(axis=0) for v in limits])
highs = np.array([v.max(axis=0) for v in limits])
records = []
for name in ('Ground | continuous timber floor','First | floor with corrected L stairwell opening',
             'Mapping v30 | Outer alley walkable floor','Mapping v30 | Rear turn walkable floor'):
    obj = scene.objects[name]
    evaluated = obj.evaluated_get(deps)
    mesh = evaluated.to_mesh()
    vs = [evaluated.matrix_world@v.co for v in mesh.vertices]
    tree = BVHTree.FromPolygons(vs,[list(p.vertices) for p in mesh.polygons])
    lo,hi = [min(v[i] for v in vs) for i in range(3)],[max(v[i] for v in vs) for i in range(3)]
    hits,missing,mismatch = 0,[],[]
    for ix in range(math.ceil((hi[0]-lo[0])/.2)):
        for iy in range(math.ceil((hi[1]-lo[1])/.2)):
            x,y = lo[0]+.1+ix*.2,lo[1]+.1+iy*.2
            location,normal,_,_ = tree.ray_cast(Vector((x,y,hi[2]+.1)),Vector((0,0,-1)),hi[2]-lo[2]+.2)
            if location is None or normal.z<.5:
                continue
            z = location.z
            p = np.array(world((x,y,z)))
            candidates = np.where((lows[:,0]<=p[0]+.02)&(highs[:,0]>=p[0]-.02)&
                                  (lows[:,1]<=p[1]+.02)&(highs[:,1]>=p[1]-.02)&
                                  (lows[:,2]<p[2]+.15*UNIT)&(highs[:,2]>p[2]-.3*UNIT))[0]
            actual = support([solids[i] for i in candidates],x,y,high=z+.15,low=z-.3)
            hits += 1
            if actual is None:
                missing.append([x,y,z])
            elif abs(actual[0]-z)>.05:
                mismatch.append({'point_BU':[x,y,z],'support_BU':actual[0],'brush':actual[1]})
    records.append({'object':name,'samples':hits,'missing':missing,'height_mismatch':mismatch})
    evaluated.to_mesh_clear()
result = {'source':str(Path(bpy.data.filepath).relative_to(ROOT)),
          'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
          'map_sha256':hashlib.sha256(map_path.read_bytes()).hexdigest(),
          'samples':sum(r['samples'] for r in records),
          'missing_count':sum(len(r['missing']) for r in records),
          'height_mismatch_count':sum(len(r['height_mismatch']) for r in records),
          'floors':records,
          'limits':'Evaluated four principal pub/alley floor surfaces on a .2 BU grid, height tolerance .05 BU. Does not prove native physics, prefab collision, navigation or all visual seams.'}
(ROOT/'build/bo3-core/visual-floor-check.json').write_text(json.dumps(result,indent=2)+'\n')
print('CORE_VISUAL_FLOOR_CHECK',result['samples'],result['missing_count'],result['height_mismatch_count'],flush=True)
