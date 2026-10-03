"""Correct render-discovered gaps, then validate and rerender the new v25 only."""
from pathlib import Path
import bpy,json,math,bmesh
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
assert Path(bpy.data.filepath).name=='pharmacie-syston-street-v25.blend'
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
dest=ROOT/'recon/v25';r=json.loads((dest/'validation.json').read_text())
coll=bpy.data.collections['STREET v25 | Catalogue-led Syston scenery']
archive=bpy.data.collections.new('ARCHIVE v25 | Review superseded scenery');archive.use_fake_user=True
def retire(ob):
    archive.objects.link(ob)
    for c in list(ob.users_collection):
        if c!=archive:c.objects.unlink(ob)
for sp in r['catalogue_frontages']:
    # Keep original anchor centre for most rows; only restore large bridge gaps.
    if sp['id'] not in ('B014','B015','B034','B037'):continue
    group=[o for o in coll.objects if o.get('catalogue_id')==sp['id']]
    anchor=next(o for o in group if 'upper facade' in o.name)
    fac=min(1,11.0/sp['width_m_estimate']);basis=anchor.matrix_world.copy()
    tr=basis@Matrix.Diagonal((fac,1,1,1))@basis.inverted()
    for ob in group:ob.matrix_world=tr@ob.matrix_world
    sp['width_m_estimate']*=fac
    sp['review_note']='Shortened bridge-adjacent facade to retain open brook/access gap'
for ob in coll.objects:
    if ob.type=='FONT' and ob.data.size==.42:ob.data.size=.60

path=[Vector(p) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']]
l=[0]
for a,b in zip(path,path[1:]):l.append(l[-1]+(b-a).length)
def frame(s,side=1,offset=0):
    i=next(i for i in range(len(path)-1) if l[i+1]>=s);u=(path[i+1]-path[i]).normalized();n=Vector((-u.y,u.x))*side;p=path[i]+u*(s-l[i])+n*offset;x=Vector((n.y,-n.x))
    return Matrix(((x.x,n.x,0,p.x),(x.y,n.y,0,p.y),(0,0,1,0),(0,0,0,1)))
new=[]
def box(name,coords,m,basis,ident):
    x0,x1,y0,y1,z0,z1=coords;me=bpy.data.meshes.new(name)
    me.from_pydata([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],[],[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]);me.materials.append(m);me.update()
    ob=bpy.data.objects.new('Syston v25 | '+ident+' | '+name,me);coll.objects.link(ob);ob.matrix_world=basis;ob['catalogue_id']=ident;ob['status']='Approximate static scenery; Blender only';new.append(ob);return ob
dark=bpy.data.materials['Syston v25 | dark metal'];cream=bpy.data.materials['Syston v25 | stone and cream'];green=bpy.data.materials['Syston v25 | retail green']
# Railings locate the bridge, use their basis and original local range.
rail=next(o for o in coll.objects if 'F003 | bridge horizontal rail' in o.name)
bridge_basis=rail.matrix_world.copy();p=bridge_basis.translation.copy()
u=Vector((bridge_basis[0][0],bridge_basis[1][0]));bridge_s=min((p-Vector((*a,0))).length+l[i] for i,a in enumerate(path[:-1]))
# A narrow channel exits both pavement edges; road remains the bridge deck.
centre=bridge_basis.copy();centre.translation-=Vector((bridge_basis[0][1]*5.5,bridge_basis[1][1]*5.5,0))
box('water under bridge',(-1.5,1.5,-13,13,-.40,-.28),bpy.data.materials['Street v22 | brook water'],centre,'F003')
for y in (-10,7):
    box('brook bank',(-2.0,-1.5,y,y+3,-.36,-.18),bpy.data.materials['Street v22 | park grass'],centre,'F003')
    box('brook bank',(1.5,2.0,y,y+3,-.36,-.18),bpy.data.materials['Street v22 | park grass'],centre,'F003')

# Pitched bus shelter roof instead of the first rectangular roof slab.
roof=next(o for o in coll.objects if 'F006 | shelter roof' in o.name);basis=roof.matrix_world.copy();retire(roof)
for sign in (-1,1):
    slab=box('pitched green shelter roof',(-2.3,2.3,0,.78,2.3,2.37),green,basis,'F006')
    # Independent roof halves meet at ridge, slope down toward their outer edge.
    for v in slab.data.vertices:
        y=v.co.y;v.co.z+=.30*(1-y/.78);v.co.y*=sign
    bm=bmesh.new();bm.from_mesh(slab.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(slab.data);bm.free()

# B&M bay Y frame, separate from the glazing.
bay=next(o for o in coll.objects if 'B027 | projecting tall bay glass' in o.name)
for sign in (-1,1):
    ob=box('upper bay diagonal',(-.025,.025,-.025,.025,0,1),dark,bay.matrix_world.copy(),'B027')
    a=Vector((0,-.51,7.22));b=Vector((sign*.80,-.51,8.475));d=b-a
    # Rotate a solid local Z beam and translate to the bay fork.
    ob.matrix_world=bay.matrix_world@Matrix.Translation(a)@d.to_track_quat('Z','Y').to_matrix().to_4x4()
    ob.scale.z=d.length

bpy.context.view_layer.update()
solids=[o for o in coll.objects if o.type=='MESH']
for ob in solids:
    bm=bmesh.new();bm.from_mesh(ob.data)
    assert all(e.is_manifold for e in bm.edges),ob.name
    assert bm.calc_volume(signed=True)>0 and ob.matrix_world.determinant()>0,ob.name;bm.free()
# Player-space sampling tests only new geometry: no scenery intrudes onto road.
deps=bpy.context.evaluated_depsgraph_get();tested=0
newset={o.name for o in coll.objects}
for s in range(18,278,2):
    for side_offset in (-2.7,0,2.7):
        bs=frame(s,1,side_offset);origin=bs.translation+Vector((0,0,1.7))
        hit,loc,n,idx,ob,m=scene.ray_cast(deps,origin,Vector((0,0,1)),distance=12)
        assert not hit or ob.name not in newset,('Road obstructed',s,side_offset,ob.name)
        tested+=1
r['closed_outward_solids']=len(solids);r['road_clearance_samples']=tested
r['review_fixes']=['Shortened four bridge-adjacent bays to restore gap','Larger geometric lettering','Pitched shelter roof','Separate brook water/banks','B&M Y frame']
(dest/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_percentage=100
scene.world=scene.world.copy();scene.world.use_nodes=True;bg=scene.world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.65;bg.inputs['Color'].default_value=(.67,.75,.86,1)
ld=bpy.data.lights.new('Temporary review sun','SUN');ld.energy=2.3;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
for cam in [o for o in scene.objects if o.name.startswith('Review v25 |')]:
    scene.camera=cam;scene.render.resolution_x=1200 if cam.data.type=='ORTHO' else 1400;scene.render.resolution_y=1600 if cam.data.type=='ORTHO' else 950
    scene.render.filepath=str(dest/(cam.name.split(' | ')[1]+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps({'closed_solids':len(solids),'clear_road_samples':tested,'frontages':len(r['catalogue_frontages'])}))
