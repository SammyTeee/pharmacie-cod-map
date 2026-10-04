"""Stream distinct GPU renders into FFmpeg; keep one scratch frame on disk."""
from pathlib import Path
import bpy,json,os,math,subprocess
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v33'
phase=os.environ.get('V33_VIDEO_PHASE','after')
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
scene.render.engine='CYCLES';scene.cycles.samples=4;scene.cycles.use_denoising=True;scene.cycles.denoiser='OPTIX'
scene.cycles.max_bounces=4;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=2
scene.cycles.transmission_bounces=2;scene.cycles.transparent_max_bounces=4
pref=bpy.context.preferences.addons['cycles'].preferences;pref.compute_device_type='OPTIX';pref.get_devices()
for device in pref.devices:device.use=device.type=='OPTIX'
scene.cycles.device='GPU';scene.render.use_persistent_data=True
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
world=bpy.data.worlds.new('Temporary v33 flight daylight');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.72,.82,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;scene.world=world
sun=bpy.data.lights.new('Temporary flight sun','SUN');sun.energy=2.5
obj=bpy.data.objects.new(sun.name,sun);scene.collection.objects.link(obj);obj.rotation_euler=(.45,-.55,-.45)
for x,y,z in ((4,4,3.8),(4,12,3.8),(5,23,3.8),(4,7,8),(4,18,8),(4,27,8)):
    light=bpy.data.lights.new('Temporary flight room fill','AREA');light.energy=180;light.size=4
    obj=bpy.data.objects.new(light.name,light);scene.collection.objects.link(obj);obj.location=(x,y,z)
data=bpy.data.cameras.new('Temporary v33 flight camera');data.lens=24;data.clip_start=.04
camera=bpy.data.objects.new(data.name,data);scene.collection.objects.link(camera);scene.camera=camera
plan=json.loads((dest/'flythrough-route.json').read_text());assert not plan['failures']
fps=12;sections=plan['sections'];duration=sum(s['duration'] for s in sections)
if phase=='before':
    fps=8
    sections=[dict(name='Stair seam before',duration=4,eyes=[(6.6,29.3,4.32),(6.6,28.7,4.62)],target=(10,31,4.6)),
              dict(name='Rear ceiling before',duration=4,eyes=[(-2.50,23.3,1.65),(-2.58,24.4,1.65)],target=(-4.5,28,4.5)),
              dict(name='Service lane before',duration=4,eyes=[(46.5,-24,1.65),(46.5,-26.5,1.65)],target=(46.5,-30.5,2.4))]
    duration=12
output=dest/('player-route-flythrough.webm' if phase=='after' else 'before-inspection.webm')
scratch=ROOT/'build'/('v33-'+phase+'-stream-frame.png')
vf=[];elapsed=0
for section in sections:
    title=section['name']
    vf.append("drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='"+title+"':fontsize=25:fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=10:x=24:y=24:enable='between(t,"+str(elapsed)+","+str(elapsed+3)+")'")
    elapsed+=section['duration']
vf.append('fps=24')
log=open(ROOT/'build'/('v33-'+phase+'-encode.log'),'w')
process=subprocess.Popen(['C:/ffmpeg/ffmpeg.exe','-hide_banner','-loglevel','error','-y',
    '-f','image2pipe','-vcodec','png','-framerate',str(fps),'-i','pipe:0','-vf',','.join(vf),
    '-c:v','libvpx-vp9','-b:v','1400k','-crf','30','-row-mt','1','-deadline','good','-cpu-used','4',
    '-pix_fmt','yuv420p','-an',str(output)],stdin=subprocess.PIPE,stderr=log,creationflags=0x08000000)
frame=0;manifest=[]
try:
    for section in sections:
        if phase=='after':
            points=[Vector(p) for p in section['feet']]
            lengths=[(b-a).length for a,b in zip(points,points[1:])];total=sum(lengths)
            def at(distance):
                distance=max(0,min(total,distance))
                for i,length in enumerate(lengths):
                    if distance<=length:return points[i].lerp(points[i+1],distance/length)
                    distance-=length
                return points[-1]
        for k in range(section['duration']*fps):
            u=k/max(1,section['duration']*fps-1)
            if phase=='after':
                eye=at(u*total)+Vector((0,0,1.65))
                target=at(min(total,u*total+1.5))+Vector((0,0,1.65))
                if (target-eye).length<.05:
                    target=eye+(points[-1]-points[-2]).normalized()
            else:
                eye=Vector(section['eyes'][0]).lerp(Vector(section['eyes'][1]),u);target=Vector(section['target'])
            camera.location=eye;camera.rotation_euler=(target-eye).to_track_quat('-Z','Y').to_euler()
            scene.render.filepath=str(scratch);bpy.ops.render.render(write_still=True)
            assert process.poll() is None,'FFmpeg stopped; inspect encode log'
            process.stdin.write(scratch.read_bytes())
            if frame%fps==0:
                bpy.data.images['Render Result'].save_render(str(dest/(phase+'-flight-%02d.png'%(frame//fps))),scene=scene)
                print('V33_FLIGHT_PROGRESS',phase,frame,duration*fps,flush=True)
            frame+=1
        manifest.append(dict(name=section['name'],start_seconds=(frame-section['duration']*fps)/fps,duration_seconds=section['duration']))
finally:
    process.stdin.close()
    code=process.wait();log.close()
assert code==0,code
assert frame==duration*fps
(dest/(phase+'-flythrough.json')).write_text(json.dumps(dict(video=output.name,duration_seconds=duration,
    resolution=[1280,720],distinct_render_fps=fps,playback_fps=24,distinct_frames=frame,
    bytes=output.stat().st_size,sections=manifest,render='GPU OptiX Cycles4 denoised; maximum four bounces',
    style='Textured player-height camera review. Continuous inside each section, cuts between sections; not a game test.',
    source=bpy.data.filepath,source_scene_saved=False),indent=2))
print('V33_FLIGHT_COMPLETE',phase,frame,output.stat().st_size,flush=True)
