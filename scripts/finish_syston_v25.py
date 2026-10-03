"""Final native render review: bridge in the open gap; Halls frontage width."""
from pathlib import Path
import bpy,json,math,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v25'
assert Path(bpy.data.filepath).name=='pharmacie-syston-street-v25.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
coll=bpy.data.collections['STREET v25 | Catalogue-led Syston scenery'];r=json.loads((dest/'validation.json').read_text())
assert not r.get('final_gap_review'), 'Apply once to the reviewed v25 checkpoint'
p=[Vector(x) for x in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']];ls=[0]
for a,b in zip(p,p[1:]):ls.append(ls[-1]+(b-a).length)
def point(s):
    i=next(i for i in range(len(p)-1) if ls[i+1]>=s);return p[i]+(p[i+1]-p[i]).normalized()*(s-ls[i])
delta=point(214)-point(200.4269)
for o in coll.objects:
    if o.get('catalogue_id')=='F003':o.matrix_world=Matrix.Translation((*delta,0))@o.matrix_world
bpy.data.objects['Review v25 | 06_bridge_player'].location+=Vector((*delta,0))
bpy.data.objects['Review v25 | 06_bridge_player']['final_bridge_framed']=True
sp=next(s for s in r['catalogue_frontages'] if s['id']=='B004');group=[o for o in coll.objects if o.get('catalogue_id')=='B004']
base=next(o for o in group if 'upper facade' in o.name).matrix_world.copy();fac=11/sp['width_m_estimate'];tr=base@Matrix.Diagonal((fac,1,1,1))@base.inverted()
for o in group:o.matrix_world=tr@o.matrix_world
sp['width_m_estimate']=11;sp['review_note']='Shortened Halls bay to restore open bridge-side space'
# Photographed GLO turns the corner with white ground-level masonry.
white=bpy.data.materials['Syston v25 | white joinery']
for o in coll.objects:
    if o.get('catalogue_id')=='B033' and o.type=='MESH' and any(x in o.name for x in ('fascia','lower plinth','front pilaster')):o.data.materials[0]=white
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
for side in (-1,1):
    centre=point(214);u=(point(215)-centre).normalized();n=Vector((-u.y,u.x))
    for s in range(-4,5,2):
        xy=centre+u*s+n*side*8.5;origin=Vector((*xy,1.7))
        hit,loc,normal,idx,ob,ma=scene.ray_cast(deps,origin,Vector((0,0,1)),distance=12)
        assert not hit,('Bridge gap blocked',side,s,ob.name)
r['final_gap_review']={'bridge_chainage_estimate_m':214,'both_sides_gap_samples':10,'halls_width_m_estimate':11,'observed_corner_finish':'GLO white ground-floor masonry'}
(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary final sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for name in ('01_syston_overview','04_bridge_shop_row','05_roundabout_approach','06_bridge_player','07_junction_player'):
    cam=bpy.data.objects['Review v25 | '+name];scene.camera=cam;scene.render.resolution_x=1200 if cam.data.type=='ORTHO' else 1400;scene.render.resolution_y=1600 if cam.data.type=='ORTHO' else 950
    scene.render.filepath=str(dest/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(r['final_gap_review']))
