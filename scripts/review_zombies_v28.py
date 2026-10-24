"""Read-only saved-scene review: stills, solid inspection flythrough and floor rays."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'recon/v28-zombies';dest.mkdir(exist_ok=True)
frames=dest/'frames';frames.mkdir(exist_ok=True)
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
dep=bpy.context.evaluated_depsgraph_get()
cams=sorted([o for o in scene.objects if o.type=='CAMERA' and o.name.startswith('Review')],key=lambda o:o.name)
inventory=[{'name':o.name,'position':list(o.location),'type':o.data.type} for o in cams]
(dest/'cameras.json').write_text(json.dumps(inventory,indent=2))
# Broad ground coverage around intended street corridors; no guess that all parcels are playable.
path=[Vector(p) for p in json.loads((ROOT/'recon/v22/validation.json').read_text())['melton_centreline']]
samples=[]
for a,b in zip(path,path[1:]):
    d=b-a;n=Vector((-d.y,d.x)).normalized()
    for i in range(math.ceil(d.length)):
        p=a+d*(i/math.ceil(d.length))
        for off in (-5,-2.5,0,2.5,5):
            q=p+n*off
            hit,loc,norm,idx,o,mat=scene.ray_cast(dep,Vector((q.x,q.y,1.65)),Vector((0,0,-1)),distance=8)
            samples.append({'xy':[q.x,q.y],'offset':off,'hit':o.name if hit else None,'z':loc.z if hit else None})
# Fixed review camera support and enclosing surfaces; openings are reported, not called leaks automatically.
camera_rays=[]
for c in cams:
    if c.data.type!='PERSP' or c.location.z>5:continue
    rays={}
    for name,d in [('down',(0,0,-1)),('up',(0,0,1)),('east',(1,0,0)),('west',(-1,0,0)),('north',(0,1,0)),('south',(0,-1,0))]:
        hit,loc,n,idx,o,m=scene.ray_cast(dep,c.location,Vector(d),distance=30)
        rays[name]={'hit':o.name if hit else None,'distance':(loc-c.location).length if hit else None}
    camera_rays.append({'camera':c.name,'position':list(c.location),'rays':rays})
(dest/'geometry-review.json').write_text(json.dumps({'checkpoint':bpy.data.filepath,'street_floor_samples':samples,'missing_floor_samples':sum(x['hit'] is None for x in samples),'camera_enclosure_rays':camera_rays,'limits':['Ray hits are visible geometry, not BO3 collision','Sky above outdoor streets is expected','Open horizontal rays may be doorways or unfinished map bounds','Sparse rays cannot certify watertight rooms or player hull clearance']},indent=2))
selected=[]
for term in ['crossing','amy_clarke','02_costa_and_town_square','06_bridge_player','01_taraj_dining','05_taraj_entry','03_taraj_bar']:
    found=next((c for c in cams if c.name.endswith(term)),None)
    if found:selected.append(found)
# Include retained pub player views by name, with fallback to nearby low cameras.
pub=[c for c in cams if c.data.type=='PERSP' and c.location.z<5 and abs(c.location.x)<20 and -15<c.location.y<40 and c not in selected]
selected+=pub[:4]
scene.render.resolution_x=960;scene.render.resolution_y=540;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
scene.world=scene.world.copy();scene.world.use_nodes=True
bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Strength'].default_value=.6
ld=bpy.data.lights.new('Temporary inspection sunlight','SUN');ld.energy=2;lo=bpy.data.objects.new(ld.name,ld);scene.collection.objects.link(lo);lo.rotation_euler=(.45,-.55,-.45)
stills=[]
for i,c in enumerate(selected):
    scene.camera=c;filename=f'{i+1:02d}_'+c.name.split('|')[-1].strip()+'.png';scene.render.filepath=str(dest/filename)
    bpy.ops.render.render(write_still=True);stills.append({'file':filename,'camera':c.name})
(dest/'stills.json').write_text(json.dumps(stills,indent=2))
# Short forward dolly per view, hard cuts between locations; intentionally solid mode for holes/silhouettes.
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.background_type='WORLD';scene.world.color=(.12,.15,.20)
scene.render.resolution_x=640;scene.render.resolution_y=360
cd=bpy.data.cameras.new('Temporary review dolly');cam=bpy.data.objects.new(cd.name,cd);scene.collection.objects.link(cam);scene.camera=cam
segments=[];frame=0
for c in selected[:9]:
    cd.lens=c.data.lens;cam.rotation_euler=c.rotation_euler
    forward=c.rotation_euler.to_quaternion()@Vector((0,0,-1))
    # Max 0.6m movement; this is an inspection camera, not a proved traversable path.
    for k in range(36):
        cam.location=c.location+forward*(k/35*.6)
        scene.render.filepath=str(frames/f'{frame:05d}.png');bpy.ops.render.render(write_still=True);frame+=1
    segments.append({'camera':c.name,'start_seconds':(frame-36)/12,'duration_seconds':3})
(dest/'video-segments.json').write_text(json.dumps({'fps':12,'frames':frame,'style':'Solid material inspection; short dolly shots with cuts, not continuous traversal','segments':segments},indent=2))
print('ZOMBIES_REVIEW_COMPLETE',len(stills),frame,flush=True)
