"""Encode reference photos for BO3; crops live in mesh UVs, originals stay intact."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references/pharmacie-syston'
OUT = ROOT / 'assets/photos'
RECIPES = {
    'frontage': ('pharmacie-arms-syston-2.jpg', (1024, 1024)),
    'bar': ('bar front.jpg', (2048, 2048)),
    'feature_wall': ('great for texture.avif', (2048, 2048)),
}


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {'purpose': 'Private BO3 prototype; source rights unresolved for distribution',
                'assets': []}
    for name, (source, size) in RECIPES.items():
        path = REF / source
        image = Image.open(path)
        original_size = image.size
        # Format/size conversion only. Preserve source composition and lettering;
        # geometry uses normalized source UVs, so square storage does not distort panels.
        image = image.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
        image.save(OUT / f'{name}.tif', compression='raw')
        manifest['assets'].append({
            'name': name, 'source': path.relative_to(ROOT).as_posix(),
            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_dimensions': original_size, 'output': f'assets/photos/{name}.tif',
            'dimensions': size, 'edits': 'RGBA TIFF encoding and Lanczos resize only; no pixel crop or repaint',
            'material': f'pharmacie_{name}', 'status': 'prepared; build/runtime tracked in MODLOG.md',
        })
    cutout = OUT / 'skeleton-cutout.png'
    if cutout.exists():
        image = Image.open(cutout).convert('RGBA').resize((1024, 2048), Image.Resampling.LANCZOS)
        image.save(OUT / 'skeleton.tif', compression='raw')
        manifest['assets'].append({
            'name': 'skeleton', 'source': 'assets/photos/skeleton-cutout.png',
            'original_reference': next(p.relative_to(ROOT).as_posix() for p in REF.glob('ey*.jpg') if Image.open(p).size == (1500, 2000)),
            'edits': 'AI background isolation of seated skeleton and dentist chair; RGBA TIFF encoding and resize',
            'dimensions': [1024, 2048], 'material': 'pharmacie_skeleton',
            'status': 'prepared; alpha-test material; build/runtime tracked in MODLOG.md',
        })
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    gdt = ['{']
    for item in manifest['assets']:
        name = item['name']
        image_name = f'i_pharmacie_{name}'
        fields = {
            'baseImage': f'texture_assets\\pharmacie\\{name}.tif',
            'imageType': 'Texture', 'type': 'image', 'semantic': 'diffuseMap',
            'coreSemantic': 'sRGB3chAlpha', 'compressionMethod': 'compressed high color',
            'clampU': '1', 'clampV': '1', 'mipMode': 'Average', 'mipBase': '1/1',
            'noMipMaps': '0', 'streamable': '0', 'colorSRGB': '0',
        }
        gdt.extend([f'\t"{image_name}" ( "image.gdf" )', '\t{'])
        gdt.extend(f'\t\t"{k}" "{v}"' for k,v in fields.items())
        gdt.append('\t}')
        fields = {
            'materialType': 'lit_alphatest_nocull' if name == 'skeleton' else 'lit_nocull',
            'materialCategory': 'Geometry', 'template': 'material.template',
            'colorMap': image_name, 'colorTint': '1 1 1 1', 'normalMap': '$normal',
            'occMap': '$white_ao', 'glossSurfaceType': '<custom>',
            'glossRangeMin': '0', 'glossRangeMax': '2',
            'surfaceType': 'wood' if name == 'bar' else 'concrete',
            'usage': 'wall', 'sort': '<default>*', 'nonColliding': '1', 'nonSolid': '1',
            'noCastShadow': '1', 'alphaTest': '0.5',
        }
        gdt.extend([f'\t"pharmacie_{name}" ( "material.gdf" )', '\t{'])
        gdt.extend(f'\t\t"{k}" "{v}"' for k,v in fields.items())
        gdt.append('\t}')
    gdt.append('}')
    (OUT / 'pharmacie.gdt').write_text('\n'.join(gdt)+'\n', encoding='utf-8')
    print(f'Prepared {len(manifest["assets"])} photo materials in {OUT}')


if __name__ == '__main__':
    prepare()
