"""Photo meshes with explicit UVs; crops do not modify reference image pixels."""
import uuid
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMESPACE = uuid.UUID('682c13ea-815e-4b1c-86ec-f8db141a1e8c')
# Pixel bounds observed in the clear 1024x751 frontage image. The walk-through
# opening matches the photographed right-hand pair of entrance doors.
FRONT_CROP = (28, 190, 1000, 674)
DOOR_PIXELS = (535, 435, 700, 674)
FRONT_WIDTH = 704
FRONT_HEIGHT = 320
DOOR_LEFT = -352 + (535-28)/972*FRONT_WIDTH
DOOR_RIGHT = -352 + (700-28)/972*FRONT_WIDTH
DOOR_HEIGHT = (674-435)/484*FRONT_HEIGHT


def mesh(number, name, material, corners, uv, nl):
    """Corners and UVs: top left, top right, bottom left, bottom right."""
    width,height = Image.open(ROOT / f'assets/photos/{material}.tif').size
    rows = [f'// brush {number}', '{', f' guid "{{{uuid.uuid5(NAMESPACE,name)}}}"',
            ' mesh', ' {', '  toolFlags;', f'  pharmacie_{material}',
            '  lightmap_gray', '  2 2 0 8']
    for row in range(2):
        rows.append('  (')
        for col in range(2):
            i = row*2+col
            x,y,z = corners[i]
            u,v = uv[i]
            rows.append(f'   v {x:g} {y:g} {z:g} t {u*width:g} {v*height:g} {col} {row}')
        rows.append('  )')
    rows.extend([' }', '}'])
    return nl.join(rows)+nl


def panels(first_number, nl):
    result=[]
    def add(name, material, corners, pixel_crop=None):
        if pixel_crop:
            source = {'frontage': 'pharmacie-arms-syston-2.jpg', 'bar': 'bar front.jpg'}[material]
            w,h = Image.open(ROOT/'references/pharmacie-syston'/source).size
            a,b,c,d = pixel_crop
            uv=((a/w,b/h),(c/w,b/h),(a/w,d/h),(c/w,d/h))
        else:
            uv=((0,0),(1,0),(0,1),(1,1))
        result.append(mesh(first_number+len(result),name,material,corners,uv,nl))
    # Three panels share one photo coordinate system; the centre door stays open.
    for name,a,c,z0,z1 in (
        ('front left',-352,DOOR_LEFT,0,320),
        ('front right',DOOR_RIGHT,352,0,320),
        ('front lintel',DOOR_LEFT,DOOR_RIGHT,DOOR_HEIGHT,320),
    ):
        crop=(28+(a+352)/704*972,674-z1/320*484,
              28+(c+352)/704*972,674-z0/320*484)
        add(name,'frontage',((a,-657,z1),(c,-657,z1),(a,-657,z0),(c,-657,z0)),crop)
    add('bar drawers','bar',((-157,65,48),(195,65,48),(-157,65,0),(195,65,0)),(50,745,1900,1230))
    add('bar upper display','bar',((-157,133,142),(195,133,142),(-157,133,52),(195,133,52)),(50,270,1900,745))
    add('west pharmacy wall','feature_wall',((-351,-400,316),(-351,100,316),(-351,-400,6),(-351,100,6)))
    add('east pharmacy wall','feature_wall',((351,140,316),(351,-360,316),(351,140,6),(351,-360,6)))
    # Front-only flat set piece facing the central aisle, without a rectangle collider.
    add('skeleton in dentist chair','skeleton',((-224,-148,126),(-224,-64,126),(-224,-148,0),(-224,-64,0)))
    return ''.join(result)
