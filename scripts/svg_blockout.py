"""Read rendered SVG footprints, not the planner's inconsistent size metadata."""
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'references/pharmacie-syston/pharmacie-layout.svg'


def footprints():
    result = {}
    for group in ET.parse(SOURCE).getroot().iter('{http://www.w3.org/2000/svg}g'):
        ident = group.get('data-id')
        if not ident:
            continue
        rect = group.find('{http://www.w3.org/2000/svg}rect')
        if rect is None:
            continue
        values = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', group.get('transform', ''))))
        cx, cy, angle = values
        if angle % 90:
            raise ValueError(f'{ident}: only quarter-turn footprints are supported')
        x, y, w, h = (float(rect.get(k, '0')) for k in ('x', 'y', 'width', 'height'))
        a = math.radians(angle)
        points = [((cx + px*math.cos(a)-py*math.sin(a)-466)*2,
                   (550-cy-px*math.sin(a)-py*math.cos(a))*2)
                  for px in (x,x+w) for py in (y,y+h)]
        result[ident] = tuple(round(v) for v in (min(p[0] for p in points), max(p[0] for p in points), min(p[1] for p in points), max(p[1] for p in points)))
    return result


def boxes():
    f = footprints()
    b = []
    def add(name, xy, bottom, top):
        b.append((name, (*xy, bottom, top)))
    add('main floor', (-368,368,-656,816), -16,0)
    add('main ceiling', (-368,368,-656,816), 320,336)
    add('west wall', (-368,-352,-656,800),0,320)
    add('east wall', (352,368,-656,816),0,320)
    # Entrance follows the visible SVG path M493 870H587.
    add('front west',(-352,54,-656,-640),0,320)
    add('front east',(242,352,-656,-640),0,320)
    add('entrance lintel',(54,242,-656,-640),208,320)
    # Small enclosed street vestibule prevents an open doorway into the void.
    add('vestibule floor',(38,258,-784,-640),-16,0)
    add('vestibule west',(38,54,-784,-656),0,320)
    add('vestibule east',(242,258,-784,-656),0,320)
    add('vestibule end',(54,242,-784,-768),0,320)
    add('vestibule roof',(38,258,-784,-656),320,336)
    add('rear west',(-352,-334,800,816),0,320)
    add('rear east',(-230,352,800,816),0,320)
    add('patio door lintel',(-334,-230,800,816),208,320)
    x0,x1,y0,y1 = f['smoking-area']
    add('patio floor',(x0-16,x1+16,800,y1+16),-16,0)
    add('patio west',(x0-16,x0,800,y1+16),0,192)
    add('patio east',(x1,x1+16,816,y1+16),0,192)
    add('patio north',(x0,x1,y1,y1+16),0,192)
    add('patio south west',(x0,-352,800,816),0,192)
    # Toilet is hollow, with a 96-unit south doorway facing the bar.
    x0,x1,y0,y1 = f['toilet']
    add('toilet west',(x0,x0+12,y0,y1),0,224)
    add('toilet east',(x1-12,x1,y0,y1),0,224)
    add('toilet back',(x0+12,x1-12,y1-12,y1),0,224)
    mid=(x0+x1)//2
    add('toilet front left',(x0+12,mid-48,y0,y0+12),0,224)
    add('toilet front right',(mid+48,x1-12,y0,y0+12),0,224)
    add('toilet lintel',(mid-48,mid+48,y0,y0+12),192,224)
    add('platform',f['raised-platform'],0,12)
    add('bar',f['bar'],0,48)
    # Rear flight follows the rotated arrow (east), joining the marked right route.
    x0,x1,y0,y1=f['stairs']
    for i in range(13):
        left=x0+i*32
        add(f'rear stair {i+1}',(left,min(left+32,x1),y0,y1),0,(i+1)*8)
    add('east landing',(x1,336,640,y1),0,104)
    for i in range(13):
        add(f'east stair {i+1}',(224,336,328+i*24,352+i*24),0,(i+1)*8)
    for ident,xy in f.items():
        if ident.startswith('table-') or ident=='added-murb8s0z':
            add(ident,xy,0,32)
    add('sofa',f['sofa'],0,28)
    add('skeleton placeholder',f['skeleton'],0,48)
    add('chairs',f['added-murb7sam'],0,24)
    return b
