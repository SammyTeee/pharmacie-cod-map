"""Conservative standing-player route checks against exported static brushes.

Uses a circumscribed 16-sided cylinder and clips its complete convex volume
against each nearby solid. Omits purchased blocker groups, so this checks the
open routes. It is source geometry verification, not BO3 movement simulation.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json
import math
import hashlib
import numpy as np
from audit_bo3_core_ground import load_solids, support, world, UNIT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'build/bo3-core'


def vertices(planes):
    normals = np.array([n for n, d in planes])
    distances = np.array([d for n, d in planes])
    result = []
    for ids in combinations(range(len(planes)), 3):
        a = normals[list(ids)]
        if abs(np.linalg.det(a)) < 1e-8:
            continue
        p = np.linalg.solve(a, distances[list(ids)])
        if np.all(normals @ p >= distances-.02):
            result.append(p)
    assert result, 'Invalid convex brush'
    return np.array(result)


def clip_faces(faces, n, d):
    n = np.asarray(n,dtype=float)
    result, cap = [], []
    for face in faces:
        new = []
        for a, b in zip(face, face[1:]+face[:1]):
            da, db = float(np.dot(n,a)-d), float(np.dot(n,b)-d)
            if da >= 0:
                new.append(a)
            if (da >= 0) != (db >= 0):
                p = a+(b-a)*(da/(da-db))
                new.append(p)
                if not any(np.linalg.norm(p-q)<.001 for q in cap):
                    cap.append(p)
        if len(new)>=3:
            result.append(new)
    if len(cap)>=3:
        centre = np.mean(cap,axis=0)
        axis = np.array((1,0,0)) if abs(n[0])<.8 else np.array((0,1,0))
        u = np.cross(n,axis)
        u /= np.linalg.norm(u)
        v = np.cross(n,u)
        cap.sort(key=lambda p: math.atan2(np.dot(p-centre,v),np.dot(p-centre,u)))
        result.append(cap)
    return result


def body_faces(x,y,z):
    # BO3 standing envelope: radius 15, height 70 engine units. Allow ordinary
    # 18-unit stair stepping, testing solid obstacles from step height to head.
    radius = 15/math.cos(math.pi/16)
    ring = [(x+radius*math.cos(i*math.tau/16),y+radius*math.sin(i*math.tau/16)) for i in range(16)]
    bottom = [np.array((a,b,z+18.05)) for a,b in ring]
    top = [np.array((a,b,z+70)) for a,b in ring]
    return [bottom,top]+[[bottom[i],bottom[(i+1)%16],top[(i+1)%16],top[i]] for i in range(16)]


def main():
    map_path = ROOT/'map_source/zm/zm_pharmacie_core65.map'
    solids = load_solids(map_path.read_text())
    bounds = []
    for index,planes in solids:
        vs = vertices(planes)
        bounds.append((vs.min(axis=0),vs.max(axis=0)))
    lows = np.array([p[0] for p in bounds])
    highs = np.array([p[1] for p in bounds])
    samples = [s for s in json.loads((ROOT/'recon/v30/checks/route-probes.json').read_text())['samples'] if s['route']!='upper_hall']
    # Extend the checked entrance out to the street and cover both street arms.
    for route,a,b in [('front_to_road',(5.5,-2,0),(5.5,-7,-.08)),
                      ('west_street',(5.5,-6.5,-.08),(-53,-6.5,-.08)),
                      ('east_street',(5.5,-6.5,-.08),(55,-6.5,-.08)),
                      ('street_to_alley',(-11.4,-6.5,-.08),(-11.4,0,0)),
                      ('aisle_left_approach',(5.5,14,0),(5.5,14.5,0)),
                      ('aisle_to_left',(5.5,14.5,0),(-2,14.5,0)),
                      ('left_passage_join',(-2,14.5,0),(-2,14,0)),
                      ('aisle_to_right',(5.5,14,0),(8.8,14,0)),
                      ('right_service_join',(8.8,21,0),(7,21.5,0)),
                      ('stair_turn',(6.6,29.75,2.667),(6.6,29,2.934)),
                      ('upper_arrival',(6.6,24.85,4.8),(7.1,24.85,4.8)),
                      ('upper_rail_clearance',(7.1,24.85,4.8),(7.1,24.4,4.8)),
                      ('upper_hall_entry',(7.1,24.4,4.8),(7.7,24.4,4.8)),
                      ('upper_hall',(7.7,24.4,4.8),(7.7,20,4.8)),
                      ('upper_hall_turn',(7.7,20,4.8),(6.5,18,4.8)),
                      ('upper_front',(6.5,18,4.8),(5.3,10,4.8)),
                      ('upper_door',(5.3,10,4.8),(5.3,6.5,4.8)),
                      ('upper_front_room',(5.3,6.5,4.8),(6.5,5,4.8))]:
        count = math.ceil(math.dist(a,b)/.15)
        for i in range(count+1):
            samples.append({'route':route,'nominal':[a[j]+(b[j]-a[j])*i/count for j in range(3)]})
    results = []
    last = {}
    for sample in samples:
        route = sample['route']
        x,y,z = sample['nominal']
        floor = support(solids,x,y,high=z+.6,low=z-.8)
        row = {'route':route,'nominal_BU':[x,y,z],'support_BU':floor[0] if floor else None,'blocking_brushes':[]}
        if floor:
            p = np.array(world((x,y,floor[0])))
            lo,hi = p+(-15.4,-15.4,18.05),p+(15.4,15.4,70)
            candidates = np.where(np.all(highs>lo+.01,axis=1)&np.all(lows<hi-.01,axis=1))[0]
            for candidate in candidates:
                index,planes = solids[candidate]
                faces = body_faces(*p)
                for n,d in planes:
                    faces = clip_faces(faces,np.array(n),d)
                    if not faces:
                        break
                if faces:
                    vs = np.array([v for face in faces for v in face])
                    if np.all(vs.max(axis=0)-vs.min(axis=0)>.02):
                        row['blocking_brushes'].append(index)
            previous = last.get(route)
            if previous and math.dist((x,y),previous[:2])<.5:
                delta = (floor[0]-previous[2])*UNIT
                if abs(delta)>18.1:
                    row['excessive_step_engine'] = delta
            last[route] = (x,y,floor[0])
        results.append(row)
    failures = [r for r in results if r['support_BU'] is None or r['blocking_brushes'] or 'excessive_step_engine' in r]
    report = {'map_sha256':hashlib.sha256(map_path.read_bytes()).hexdigest(),'samples':len(results),
              'route_samples':dict(Counter(r['route'] for r in results)),
              'failure_count':len(failures),'failures_by_route':dict(Counter(r['route'] for r in failures)),
              'failures':failures,'results':results,
              'limits':'Open-route static exported brushes only; conservative 16-sided standing cylinder, radius 15/height 70/step 18 engine units. Does not expand stock prefab collision, run native player physics, prove AI/co-op or visually inspect seams.'}
    (OUT/'route-clearance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('samples','failure_count','failures_by_route')}),flush=True)


if __name__=='__main__':
    main()
