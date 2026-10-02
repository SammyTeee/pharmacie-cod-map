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
    # Upper floor doubles as the downstairs ceiling. Leave an L-shaped stairwell.
    sx0,sx1,sy0,sy1 = f['stairs']
    for name,xy in (
        ('front',(-368,368,-656,328)),
        ('middle west',(-368,224,328,sy0)),
        ('middle east',(336,368,328,sy0)),
        ('rear west',(-368,sx0,sy0,sy1)),
        ('rear east',(336,368,sy0,sy1)),
        ('back',(-368,368,sy1,816)),
    ):
        add('upstairs floor '+name,xy,320,336)
    add('upstairs roof',(-368,368,-656,816),640,656)
    add('upstairs west wall',(-368,-352,-656,816),320,640)
    add('upstairs east wall',(352,368,-656,816),320,640)
    add('upstairs front wall',(-352,352,-656,-640),320,640)
    add('upstairs rear wall',(-352,352,800,816),320,640)
    add('west wall', (-368,-352,-656,800),0,320)
    add('east wall', (352,368,-656,816),0,320)
    # Sam requested the door opening at the actual position in the photo.
    from photo_panels import DOOR_LEFT, DOOR_RIGHT, DOOR_HEIGHT
    add('front west',(-352,DOOR_LEFT,-656,-640),0,320)
    add('front east',(DOOR_RIGHT,352,-656,-640),0,320)
    add('entrance lintel',(DOOR_LEFT,DOOR_RIGHT,-656,-640),DOOR_HEIGHT,320)
    # Bounded outdoor strip lets players step back and see the full frontage.
    add('forecourt floor',(-368,368,-1024,-640),-16,0)
    add('forecourt west',(-368,-352,-1024,-656),0,160)
    add('forecourt east',(352,368,-1024,-656),0,160)
    add('forecourt end',(-352,352,-1024,-1008),0,160)
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
    add('bar countertop',(-161,199,62,138),48,52)
    # Climb north on the east flight, turn left at 168 units, then climb west
    # to the upper floor at 336. Each rise is below the 18-unit step standard.
    x0,x1,y0,y1=f['stairs']
    for i in range(13):
        left=x0+i*32
        add(f'rear stair {i+1}',(left,min(left+32,x1),y0,y1),0,336-i*168/13)
    add('east landing',(x1,336,640,y1),0,168)
    for i in range(13):
        add(f'east stair {i+1}',(224,336,328+i*24,352+i*24),0,(i+1)*168/13)
    def table(name,xy,base=0):
        x0,x1,y0,y1=xy
        add(name+' tabletop',xy,base+28,base+32)
        for j,(x,y) in enumerate(((x0+8,y0+8),(x1-14,y0+8),(x0+8,y1-14),(x1-14,y1-14))):
            add(name+f' leg {j}',(x,x+6,y,y+6),base,base+28)
        # Two simple wooden seats per table, with backs, outside the tabletop.
        mid=(x0+x1)//2
        for j,y in enumerate((y0-32,y1+8)):
            add(name+f' chair {j} seat',(mid-12,mid+12,y,y+24),base,base+18)
            back=y if j==0 else y+20
            add(name+f' chair {j} back',(mid-12,mid+12,back,back+4),base+18,base+36)
    for ident,xy in f.items():
        if ident.startswith('table-') or ident=='added-murb8s0z':
            table(ident,xy)
    table('table extra west',(-304,-200,184,260))
    table('table extra platform',(176,280,-380,-304),12)
    table('table extra patio',(-448,-344,872,948))
    add('sofa',f['sofa'],0,28)
    add('chairs',f['added-murb7sam'],0,24)
    return b
