"""Sample static collision support across the core, with purchased gates omitted.

Checks exported convex half-spaces, not rendered models. Native runtime traces
and Sam's manual traversal remain separate acceptance steps.
"""
from pathlib import Path
import argparse
import json
import math
import re
from bo3_map_io import parse_map_entities
from generate_blockout import kv

ROOT = Path(__file__).resolve().parents[1]
UNIT = 100/2.54
NUM = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
TRIPLE = re.compile(r'\(\s*('+NUM+r')\s+('+NUM+r')\s+('+NUM+r')\s*\)')


def world(p):
    return ((p[0]-3.5)*UNIT,(p[1]-10)*UNIT,p[2]*UNIT)


def load_solids(text):
    entities = parse_map_entities(text)
    blocks = [b for _,_,b in entities if kv(b,'classname')=='worldspawn' or
              kv(b,'classname')=='script_brushmodel' and not kv(b,'targetname')]
    solids = []
    for block in blocks:
        for match in re.finditer(r'(?ms)^// brush (\d+)\n\{.*?^\}\n?',block):
            b = match[0]
            if 'nonColliding' in b or '\n mesh\n' in b or re.search(r'\)\s+(sky|trigger)\s',b):
                continue
            planes = []
            for line in b.splitlines():
                p = TRIPLE.findall(line)
                if len(p)!=3:
                    continue
                a,c,d = [tuple(map(float,v)) for v in p]
                u,v = [c[i]-a[i] for i in range(3)],[d[i]-a[i] for i in range(3)]
                n = [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
                length = math.sqrt(sum(x*x for x in n))
                if length:
                    n = [x/length for x in n]
                    planes.append((n,sum(n[i]*a[i] for i in range(3))))
            if len(planes)>=4:
                solids.append((int(match[1]),planes))
    return solids


def support(solids,x,y,high=.35,low=-1):
    p = world((x,y,0))
    hits = []
    for index,planes in solids:
        bottom,top = -math.inf,math.inf
        for n,d in planes:
            rhs = d-n[0]*p[0]-n[1]*p[1]
            if abs(n[2]) < 1e-7:
                if rhs > .02:
                    break
            elif n[2]>0:
                bottom = max(bottom,rhs/n[2])
            else:
                top = min(top,rhs/n[2])
        else:
            if bottom < top and low*UNIT <= top <= high*UNIT:
                hits.append((top/UNIT,index))
    return max(hits) if hits else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label',default='ground-repair')
    parser.add_argument('--require-pass',action='store_true')
    args = parser.parse_args()
    solids = load_solids((ROOT/'map_source/zm/zm_pharmacie_core65.map').read_text())
    samples = []
    # A broad grid checks void protection even in closed/scenery plots.
    for ix in range(246):
        for iy in range(136):
            samples.append(('core_grid',-54.75+ix*.5,-29.75+iy*.5))
    # Dense front route and body-width offsets span floor, doorway, pavement,
    # kerb and road. Side samples may be inside a wall; this is support only.
    for i in range(153):
        y = 3.2-i*.1
        for x in (5.08,5.5,5.92):
            samples.append(('front_exit',x,y))
    for i in range(441):
        y = -11+i*.1
        for x in (-12.4,-11.8,-11.2):
            samples.append(('alley',x,y))
    missing,heights = [],[]
    for tag,x,y in samples:
        hit = support(solids,x,y)
        if hit is None:
            missing.append({'route':tag,'xy_BU':[round(x,4),round(y,4)]})
        elif tag!='core_grid':
            heights.append({'route':tag,'xy_BU':[round(x,4),round(y,4)],'support_z_BU':hit[0],'brush':hit[1]})
    report = {'label':args.label,'samples':len(samples),'missing_count':len(missing),
              'missing_by_route':{tag:sum(s['route']==tag for s in missing) for tag in ('core_grid','front_exit','alley')},
              'missing':missing,'route_support':heights,
              'limits':'Source vertical support only. Does not prove player body clearance, visual seams, purchases or actual runtime collision.'}
    path = ROOT/'build/bo3-core'/(args.label+'.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('samples','missing_count','missing_by_route')}))
    if args.require_pass:
        assert not missing,'Unsupported core ground samples'


if __name__=='__main__':
    main()
