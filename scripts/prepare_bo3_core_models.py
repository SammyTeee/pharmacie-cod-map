"""Prepare BO3 rigid models, native-resolution photo TIFFs, GDT and placements.

Consumes export_bo3_core.py and bake_bo3_core.py output. Writes only build/.
No engine install writes. Unknown/unbaked materials fail instead of losing detail.
"""
from pathlib import Path
from collections import defaultdict, Counter
import hashlib
import json
import math
import subprocess
import argparse
from PIL import Image
from bo3_xmodel_format import validate_model_binary

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/bo3-core'
UNIT = 100 / 2.54
SHIFT = (-3.5, -10, 0)


def number(x):
    if not math.isfinite(x):
        raise ValueError('Non-finite export value')
    return format(x, '.9f').rstrip('0').rstrip('.') or '0'


def gdt(name, kind, values):
    lines = []
    for k,v in values.items():
        value = str(v).replace('\\','\\\\').replace('"','\\"')
        lines.append(f'\t"{k}" "{value}"\n')
    return f'"{name}" ( "{kind}.gdf" )\n{{\n' + ''.join(lines) + '}\n'


def linear_srgb(x):
    return round(255 * max(0, min(1, 12.92*x if x <= .0031308 else 1.055*x**(1/2.4)-.055)))


def write_model(path, records, origin):
    verts = [p for material,tri,constant in records for p in tri]
    names = sorted({material for material,tri,constant in records})
    material_ids = {name:i for i,name in enumerate(names)}
    assert len(names) < 256 and len(verts) <= 65535
    with path.open('w', newline='\n') as f:
        f.write('MODEL\nVERSION 7\nNUMBONES 1\nBONE 0 -1 "tag_origin"\n\n')
        f.write('BONE 0\nOFFSET 0 0 0\nSCALE 1 1 1\nX 1 0 0\nY 0 1 0\nZ 0 0 1\n\n')
        f.write(f'NUMVERTS {len(verts)}\n')
        for i, p in enumerate(verts):
            xyz = ' '.join(number((p[j]-origin[j])*UNIT) for j in range(3))
            f.write(f'VERT {i}\nOFFSET {xyz}\nBONES 1\nBONE 0 1\n')
        f.write(f'NUMFACES {len(records)}\n')
        for ti, (material,tri,constant_colour) in enumerate(records):
            f.write(f'TRI 0 {material_ids[material]} 0 0\n')
            if constant_colour:
                # Untextured Blender objects often have absent/collapsed UVs.
                # Give the uniform colour texture a valid tangent basis, without
                # altering image/baked UVs or any geometric coordinate.
                a = [tri[1][i]-tri[0][i] for i in range(3)]
                b = [tri[2][i]-tri[0][i] for i in range(3)]
                cross = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
                drop = max(range(3),key=lambda i:abs(cross[i]))
                axes = [i for i in range(3) if i != drop]
            # XModel uses clockwise triangles and top-origin image V.
            for ci in (0, 2, 1):
                p = tri[ci]
                norm = math.sqrt(sum(x*x for x in p[3:6]))
                if norm < 1e-8:
                    a = [tri[1][i]-tri[0][i] for i in range(3)]
                    b = [tri[2][i]-tri[0][i] for i in range(3)]
                    n = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
                    norm = math.sqrt(sum(x*x for x in n))
                    if norm < 1e-12:
                        raise ValueError('Degenerate model triangle')
                else:
                    n = p[3:6]
                normal = ' '.join(number(x/norm) for x in n)
                u,v = (p[axes[0]],p[axes[1]]) if constant_colour else p[6:8]
                f.write(f'VERT {ti*3+ci}\nNORMAL {normal}\nCOLOR 1 1 1 1\nUV 1 {number(u)} {number(1-v)}\n')
        f.write(f'NUMOBJECTS 1\nOBJECT 0 "core"\nNUMMATERIALS {len(names)}\n')
        for i,material in enumerate(names):
            f.write(f'MATERIAL {i} "{material}" "Lambert" "$none.tga"\n')
            f.write('COLOR 1 1 1 1\nTRANSPARENCY 0 0 0 1\nAMBIENTCOLOR 0 0 0 1\nINCANDESCENCE 0 0 0 1\nCOEFFS .8 0\nGLOW 0 0\nREFRACTIVE 6 1\nSPECULARCOLOR -1 -1 -1 1\nREFLECTIVECOLOR -1 -1 -1 1\nREFLECTIVE -1 1\nBLINN -1 -1\nPHONG -1\n')


def extents(items):
    lo = [min(p[i] for _,tri,_ in items for p in tri) for i in range(3)]
    hi = [max(p[i] for _,tri,_ in items for p in tri) for i in range(3)]
    return lo,hi


def volumetric(items):
    lo,hi = extents(items)
    return all(b-a > .0001 for a,b in zip(lo,hi))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--export2bin', type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((OUT/'manifest.json').read_text())
    blocks, images, models = [], [], []
    textures = OUT/'textures'
    model_dir = OUT/'models-v2'
    textures.mkdir(exist_ok=True)
    model_dir.mkdir(exist_ok=True)
    spatial = defaultdict(list)
    for info in manifest['materials']:
        asset = info['asset']
        if not info.get('triangles'):
            continue
        if info['kind'] == 'bake':
            raise RuntimeError('Unbaked material: ' + info['name'])
        if info['kind'] in ('image', 'baked_image'):
            source = ROOT / info['source']
            with Image.open(source) as im:
                im = im.convert('RGBA')
                native_dims = im.size
                transparent = im.getchannel('A').getextrema()[0] < 255
                dims = tuple(2**math.ceil(math.log2(v)) for v in native_dims)
                image_pixels = im.copy()
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            if info.get('source_sha256') and source_hash != info['source_sha256']:
                raise RuntimeError('Changed photo source bytes')
        elif info['kind'] == 'constant':
            dims, native_dims, transparent, source_hash = (4, 4), (4, 4), False, None
            Image.new('RGB', dims, tuple(linear_srgb(c) for c in info['color_linear'][:3])).save(textures/(asset+'.tif'))
        else:
            raise RuntimeError('Unsupported material: ' + repr(info))
        image_name = 'i_' + asset
        tris = json.loads((OUT/(asset+'.json')).read_text())
        outside_uv = any(p[6] < -1e-6 or p[6] > 1.000001 or p[7] < -1e-6 or p[7] > 1.000001 for t in tris for p in t)
        repeat = info.get('extension') == 'REPEAT' and outside_uv
        if info['kind'] in ('image', 'baked_image'):
            if native_dims != dims and repeat:
                raise RuntimeError('Non-power-of-two repeated image needs explicit resampling: '+info['name'])
            if native_dims != dims:
                # Add storage padding, never resize the photographed texels.
                w, h = native_dims
                padded = Image.new('RGBA', dims)
                padded.paste(image_pixels, (0, 0))
                padded.paste(image_pixels.crop((w-1,0,w,h)).resize((dims[0]-w,h)), (w,0)) if dims[0] > w else None
                padded.paste(padded.crop((0,h-1,dims[0],h)).resize((dims[0],dims[1]-h)), (0,h)) if dims[1] > h else None
                image_pixels = padded
                for tri in tris:
                    for p in tri:
                        p[6] = p[6]*w/dims[0]
                        p[7] = 1-(1-p[7])*h/dims[1]
            image_pixels.save(textures/(asset+'.tif'), compression='tiff_lzw')
        blocks.append(gdt(image_name, 'image', {'baseImage':f'texture_assets\\pharmacie_core65\\{asset}.tif',
            'imageType':'Texture', 'type':'image', 'semantic':'diffuseMap', 'coreSemantic':'sRGB3chAlpha',
            'compressionMethod':'compressed high color', 'clampU':int(not repeat), 'clampV':int(not repeat),
            'mipMode':'Average', 'mipBase':'1/1', 'noMipMaps':'0', 'streamable':'0', 'colorSRGB':'0'}))
        blocks.append(gdt(asset, 'material', {'materialType':'lit_alphatest_nocull' if transparent else 'lit_nocull',
            'materialCategory':'Geometry', 'template':'material.template', 'colorMap':image_name, 'colorTint':'1 1 1 1',
            'normalMap':'$normal', 'occMap':'$white_ao', 'glossSurfaceType':'<custom>', 'glossRangeMin':'0',
            'glossRangeMax':'2', 'surfaceType':'concrete', 'usage':'wall', 'sort':'<default>*',
            'nonColliding':'1', 'nonSolid':'1', 'noCastShadow':'0', 'alphaTest':'0.5' if transparent else 'Always',
            'filterColor':'aniso8x (mip linear)', 'tileColor':'tile both' if repeat else 'no tile'}))
        images.append({'material':info['name'], 'asset':asset, 'kind':info['kind'], 'dimensions':dims, 'native_dimensions':native_dims,
                       'source_sha256':source_hash, 'alpha_test':transparent, 'repeating':repeat,
                       'tiff_sha256':hashlib.sha256((textures/(asset+'.tif')).read_bytes()).hexdigest()})
        for tri in tris:
            center = [sum(v[i] for v in tri)/3 for i in range(3)]
            spatial[(math.floor(center[0]/16), math.floor(center[1]/16), math.floor(center[2]/8))].append((asset,tri,info['kind']=='constant'))
        print('MODEL_MATERIAL', info['name'], len(tris), flush=True)
    chunks = []
    for grid,items in sorted(spatial.items()):
        parts = math.ceil(len(items)/18000)
        for part in range(parts):
            chunks.append({'key':(grid,part),'items':items[part::parts]})
    good = [c for c in chunks if volumetric(c['items'])]
    flat = [c for c in chunks if not volumetric(c['items'])]
    if not good:
        raise RuntimeError('No volumetric chunk available for planar-surface grouping')
    for c in flat:
        lo,hi = extents(c['items'])
        center = [(a+b)/2 for a,b in zip(lo,hi)]
        candidates = [g for g in good if len(g['items'])+len(c['items']) <= 20000]
        if not candidates:
            raise RuntimeError('Cannot merge planar chunk within model vertex budget')
        def distance(g):
            a,b = extents(g['items'])
            return sum(((a[i]+b[i])/2-center[i])**2 for i in range(3))
        target = min(candidates,key=distance)
        target['items'].extend(c['items'])
    for chunk in good:
        items = chunk['items']
        lo,hi = extents(items)
        origin = [(a+b)/2 for a,b in zip(lo,hi)]
        key = 'pc65_core_'+hashlib.sha256(repr(chunk['key']).encode()).hexdigest()[:12]
        path = model_dir/(key+'.xmodel_export')
        write_model(path,items,origin)
        blocks.append(gdt(key,'xmodel',{'type':'rigid','filename':f'pharmacie_core65\\{key}.xmodel_bin','BulletCollisionLOD':'None'}))
        models.append({'asset':key,'materials':sorted({m for m,t,c in items}),'triangles':len(items),
                       'origin_engine':[(origin[i]+SHIFT[i])*UNIT for i in range(3)],
                       'source_origin_BU':origin,'bounds_BU':[lo,hi]})
    # Batch mode dispatches the .xmodel_export token converter. Explicit input
    # + output mode merely compresses text on this installed executable.
    result = subprocess.run([str(args.export2bin), '/v', '*.xmodel_export'], cwd=model_dir, capture_output=True, text=True)
    (OUT/'export2bin.log').write_text(result.stdout+result.stderr)
    if result.returncode != 0 or 'ERROR:' in result.stdout+result.stderr:
        raise RuntimeError('export2bin batch failed: '+result.stdout+result.stderr)
    for model in models:
        binary = model_dir/(model['asset']+'.xmodel_bin')
        validate_model_binary(binary)
        model['sha256'] = hashlib.sha256(binary.read_bytes()).hexdigest()
    (OUT/'pharmacie_core65.gdt').write_text('{\n'+''.join(blocks)+'}\n')
    report = {'source':manifest['source'], 'source_sha256':manifest['source_sha256'],
              'bounds_BU':manifest['bounds_BU'], 'images':images, 'models':models, 'model_directory':'models-v2',
              'planar_chunks_merged':len(flat),
              'source_objects':manifest['objects'], 'triangles':sum(m['triangles'] for m in models),
              'material_kinds':dict(Counter(i['kind'] for i in images)),
              'transform':'engine = (BU + (-3.5,-10,0)) * 39.37007874015748; model-local origins restored by entity placement',
              'limits':['export2bin acceptance only; compiler/lighting/runtime are separate gates.',
                        'Uniform-colour materials receive planar UVs for a valid tangent basis; image and baked UVs are retained.',
                        'Base-colour preserved/baked; procedural normal, metallic, roughness and glass response need BO3 adaptation.',
                        'Visual meshes have separate gameplay collision; no automatic decoration collision.']}
    (OUT/'model-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print('MODELS_DONE', len(models), report['triangles'])


if __name__ == '__main__':
    main()
