"""Capture an overlapping 360 sweep at each Street View stop and walk the route.

Route is authored geographic waypoints. Firefox is visibly driven; original
screenshots and URL metadata are written by firefox_capture. No image API.
"""
from pathlib import Path
import json,math,time,argparse,re,sys
import firefox_capture as F
from math import radians,sin,cos,atan2,sqrt
from PIL import ImageChops,ImageStat
ROOT=F.ROOT
def bearing(a,b):
    la,lb=radians(a[0]),radians(b[0]);dl=radians(b[1]-a[1])
    return (math.degrees(atan2(sin(dl)*cos(lb),cos(la)*sin(lb)-sin(la)*cos(lb)*cos(dl)))+360)%360
def distance(a,b):
    la,lb=radians(a[0]),radians(b[0]);dl=radians(b[1]-a[1]);dp=lb-la
    h=sin(dp/2)**2+cos(la)*cos(lb)*sin(dl/2)**2
    return 6371008.8*2*atan2(sqrt(h),sqrt(max(0,1-h)))
def stopped():
    if (F.BASE/'STOP').exists():raise RuntimeError('STOP marker exists; input stopped')
def meta():
    m=F.parse_url(F.read_url())
    if 'latitude' not in m or 'panorama_id' not in m:raise RuntimeError('Resolved panorama URL required; stop rather than guess')
    return m
def url_view(m,h,pitch=5,fov=90):
    # Keep known panorama/position, but set the main visible viewport angles.
    url=re.sub(r'(@-?[\d.]+,-?[\d.]+,3a,)[\d.]+y,[\d.]+h,[\d.]+t',lambda x:x[1]+f'{fov}y,{h%360:.2f}h,{pitch+90:.2f}t',m['url'])
    # Older panoramas can restore angles from the encoded viewer thumbnail state.
    # Keep both copies consistent; navigation still loads the visible Maps page.
    url=re.sub(r'(yaw%3D)-?[\d.]+',lambda x:x[1]+f'{h%360:.2f}',url)
    return re.sub(r'(pitch%3D)-?[\d.]+',lambda x:x[1]+f'{-pitch:.2f}',url)
def stable(minimum=.7,maximum=4):
    time.sleep(minimum);old=F.grab()[0].resize((96,48));start=time.monotonic();same=0
    while time.monotonic()-start<maximum:
        stopped();time.sleep(.4);new=F.grab()[0].resize((96,48));change=sum(ImageStat.Stat(ImageChops.difference(old,new)).mean)/3
        same=same+1 if change<1.2 else 0
        if same>=2:return
        old=new
def turn_to(target):
    original_id=None
    for _ in range(4):
        stopped();m=meta();error=(target-m['heading_degrees']+180)%360-180
        original_id=original_id or m['panorama_id']
        if m['panorama_id']!=original_id:raise RuntimeError('Panorama moved during rotation; stop before mislabelling')
        if abs(error)<.4:return m
        h,t,r=F.focus();gain=.09318*m['fov_degrees']/75
        dx=max(-(r.right-r.left)*.38,min((r.right-r.left)*.38,-error/gain))
        F.drag(round(dx),0)
    return meta()
def sweep(stop,travel_heading,details=True):
    stopped();m=meta();F.navigate(url_view(m,travel_heading,5,90),2.3);stable(.6,3)
    expected_id=m['panorama_id']
    for offset,role in [(0,'road-forward'),(45,'right-forward-angle'),(90,'right-frontage'),(135,'right-rear-angle'),(180,'road-backward'),(225,'left-rear-angle'),(270,'left-frontage'),(315,'left-forward-angle')]:
        turn_to((travel_heading+offset)%360);stable(.5,2)
        F.capture(f'{stop}-{role}',stop=stop,role=role,notes='Overlapping visible panorama sweep; camera coordinates are URL viewpoint, facade dimensions not measured',expected_panorama=expected_id)
    if details:
        for offset,role,pitch,fov in [(90,'right-frontage-detail',7,50),(270,'left-frontage-detail',7,50),(90,'right-pavement-detail',-15,80),(270,'left-pavement-detail',-15,80)]:
            stopped();m=meta();F.navigate(url_view(m,travel_heading+offset,pitch,fov),2.3);stable(.6,3)
            turn_to((travel_heading+offset)%360)
            F.capture(f'{stop}-{role}',stop=stop,role=role,notes='Detail view of frontage or roadside; context/occlusion may still require review',expected_panorama=expected_id)
    return meta()
def forward(heading):
    stopped();m=meta();F.navigate(url_view(m,heading,0,90),1.8);stable(.5,2)
    # Tab directly to the panorama canvas without clicking a projected scene point.
    # A single click in Street View can itself move the panorama; use a zero-motion
    # drag to give the viewport focus, then the Up key, and verify location changed.
    h,t,r=F.focus();F.pg.moveTo(r.left+(r.right-r.left)*.60,r.top+190);F.pg.mouseDown();F.pg.moveRel(2,0,duration=.1);F.pg.mouseUp();F.pg.press('up');time.sleep(2.8)
    after=meta()
    if after['panorama_id']==m['panorama_id']:
        F.pg.press('up');time.sleep(2.5);after=meta()
    if after['panorama_id']==m['panorama_id']:raise RuntimeError('Street View step did not move; requires visible review')
    return after
def run(route,max_stops,details,start_label):
    F.BASE.mkdir(parents=True,exist_ok=True);state_file=F.BASE/'walk-state.json';waypoints=route['waypoints'];index=0
    state=json.loads(state_file.read_text()) if state_file.exists() else {'completed_stops':[],'route':route,'waypoint_index':0}
    state['route']=route
    index=state.get('waypoint_index',0)
    previous=None
    for _ in range(max_stops):
        stopped();m=meta();pos=(m['latitude'],m['longitude'])
        while index<len(waypoints)-1 and distance(pos,waypoints[index]['position'])<waypoints[index].get('arrival_radius_m',14):index+=1
        target=waypoints[index];heading=bearing(pos,target['position'])
        stop=f'{start_label}-{len(state["completed_stops"])+1:03d}'
        if any(x['panorama_id']==m['panorama_id'] for x in state['completed_stops']):
            if previous is None and state['completed_stops'][-1]['panorama_id']==m['panorama_id']:
                if state.get('status')=='endpoint-reached':
                    print(json.dumps({'event':'already-complete','captured_stops':len(state['completed_stops'])}),flush=True);return
                after=forward(heading);previous=pos
                if distance(pos,(after['latitude'],after['longitude']))>55:raise RuntimeError('Unexpected resume jump over 55m')
                m=after;pos=(m['latitude'],m['longitude']);heading=bearing(pos,target['position'])
            else:raise RuntimeError('Already captured panorama reached; navigation loop stopped')
        print(json.dumps({'event':'stop-start','stop':stop,'position':pos,'pano':m['panorama_id'],'target':target['name'],'heading':heading}),flush=True)
        sweep(stop,heading,details)
        state['completed_stops'].append({'stop':stop,'latitude':pos[0],'longitude':pos[1],'panorama_id':m['panorama_id'],'travel_heading':heading,'target':target['name']});state['waypoint_index']=index
        state_file.write_text(json.dumps(state,indent=2)+'\n')
        print(json.dumps({'event':'stop-complete','stop':stop,'captured_stops':len(state['completed_stops'])}),flush=True)
        if index==len(waypoints)-1 and distance(pos,target['position'])<target.get('arrival_radius_m',14):
            state['status']='endpoint-reached';state_file.write_text(json.dumps(state,indent=2)+'\n');return
        after=forward(heading);previous=pos
        if distance(pos,(after['latitude'],after['longitude']))>55:raise RuntimeError('Unexpected jump over 55m; review before continuing')
    print(json.dumps({'event':'batch-complete','stops':max_stops,'next_position':meta()}),flush=True)
def main():
    p=argparse.ArgumentParser();p.add_argument('--route',required=True);p.add_argument('--stops',type=int,default=3);p.add_argument('--no-details',action='store_true');p.add_argument('--label',default='route');p.add_argument('--single-sweep',type=float);p.add_argument('--advance-only',type=float);p.add_argument('--retake-stop');a=p.parse_args()
    if a.retake_stop:
        state=json.loads((F.BASE/'walk-state.json').read_text())
        stop=next(s for s in state['completed_stops'] if s['stop']==a.retake_stop)
        records=[json.loads(line) for line in (F.BASE/'manifest.jsonl').read_text(encoding='utf8').splitlines()]
        record=next(r for r in records if r['stop']==a.retake_stop and r['metadata'].get('panorama_id')==stop['panorama_id'])
        F.navigate(url_view(record['metadata'],stop['travel_heading']),3);stable()
        sweep('retake-'+a.retake_stop,stop['travel_heading'],not a.no_details)
    elif a.advance_only is not None:print(json.dumps(forward(a.advance_only)),flush=True)
    elif a.single_sweep is not None:sweep(a.label,a.single_sweep,not a.no_details)
    else:run(json.loads(Path(a.route).read_text()),a.stops,not a.no_details,a.label)
if __name__=='__main__':
    with F.driver_lock():main()
