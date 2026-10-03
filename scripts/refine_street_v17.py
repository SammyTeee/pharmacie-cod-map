"""Reviewed live refinements; initial v17 preserved as a safety copy."""
from pathlib import Path
import bpy,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
scene=bpy.data.scenes['03 Both floors - assembled exterior'];bpy.context.window.scene=scene
assert not scene.get('v17_review_refined'), 'Already refined; use a new version for further changes'
backup=ROOT/'assets/blender/pharmacie-v17-before-review-refinements.blend'
if not backup.exists():bpy.ops.wm.save_as_mainfile(filepath=str(backup),copy=True)
for name,old,new in [('Wreake Valley Flooring',8.3,9.5),('Syston Dry Cleaners',8.3,9.6),('Nail and Spa shop',7.9,9.2)]:
    for o in scene.objects:
        if not o.name.startswith('Street v17 | '+name) or o.type!='MESH':continue
        for v in o.data.vertices:
            if 'isolated facade' in o.name or 'solid scenery mass' in o.name:v.co.z*=new/old
            elif any(s in o.name for s in ('pitched slate roof','gutter','chimney')):v.co.z+=new-old
            elif 'downpipe' in o.name and v.co.z>1:v.co.z+=new-old
for v in bpy.data.objects['Street v17 | Pharmacie shared terrace pitched slate roof'].data.vertices:v.co.z+=1.2
# A procedural brick preview supplies visible coursing without copying game assets.
# Mark it explicitly: game export must bake/replace this shader before conversion.
brick=bpy.data.materials['Street v17 | warm red brick']
nodes=brick.node_tree.nodes;links=brick.node_tree.links
tex=nodes.new('ShaderNodeTexBrick');tex.inputs['Color1'].default_value=(.28,.105,.047,1);tex.inputs['Color2'].default_value=(.39,.16,.075,1);tex.inputs['Mortar'].default_value=(.17,.16,.14,1)
tex.inputs['Scale'].default_value=1;tex.inputs['Brick Width'].default_value=.33;tex.inputs['Row Height'].default_value=.14;tex.inputs['Mortar Size'].default_value=.012
coord=nodes.new('ShaderNodeTexCoord');separate=nodes.new('ShaderNodeSeparateXYZ');combine=nodes.new('ShaderNodeCombineXYZ')
links.new(coord.outputs['Object'],separate.inputs[0]);links.new(separate.outputs['X'],combine.inputs['X']);links.new(separate.outputs['Z'],combine.inputs['Y']);links.new(separate.outputs['Y'],combine.inputs['Z']);links.new(combine.outputs[0],tex.inputs['Vector']);links.new(tex.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
brick['export_requirement']='Procedural review material; bake or replace with BO3 texture before conversion'
geometry=nodes.new('ShaderNodeNewGeometry');normal=nodes.new('ShaderNodeSeparateXYZ');links.new(geometry.outputs['Normal'],normal.inputs[0])
absx=nodes.new('ShaderNodeMath');absx.operation='ABSOLUTE';links.new(normal.outputs['X'],absx.inputs[0])
absy=nodes.new('ShaderNodeMath');absy.operation='ABSOLUTE';links.new(normal.outputs['Y'],absy.inputs[0])
alongx=nodes.new('ShaderNodeMath');alongx.operation='MULTIPLY';links.new(separate.outputs['X'],alongx.inputs[0]);links.new(absy.outputs[0],alongx.inputs[1])
alongy=nodes.new('ShaderNodeMath');alongy.operation='MULTIPLY';links.new(separate.outputs['Y'],alongy.inputs[0]);links.new(absx.outputs[0],alongy.inputs[1])
add=nodes.new('ShaderNodeMath');add.operation='ADD';links.new(alongx.outputs[0],add.inputs[0]);links.new(alongy.outputs[0],add.inputs[1]);links.new(add.outputs[0],combine.inputs['X'])
for o in scene.objects:
    if o.name.startswith('Front | upper brick'):
        o.data.materials.clear();o.data.materials.append(brick)
for name,pos,target,lens in [('Pub frontage',(4,-8.5,4.8),(4,0,4.7),14),('Whole street',(18,-6,52),(18,-6,0),19),('Alley and rear route',(-25,21,24),(-9,16,0),23)]:
    o=bpy.data.objects['Review v17 | '+name];o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.data.lens=lens
scene.camera=bpy.data.objects['Review v17 | Pub frontage']
scene.camera.data.lens=11
top=bpy.data.objects['Review v17 | Whole street'];top.location=(18,1.5,65);top.rotation_euler=(Vector((18,1.5,0))-top.location).to_track_quat('-Z','Y').to_euler();top.data.type='ORTHO';top.data.ortho_scale=115
# Junction branch joins the road edge; overlapping asphalt faces cause z-fighting.
branch=bpy.data.objects['Street v17 | Fox junction branch road']
for v in branch.data.vertices:
    if v.co.y>-10.4:v.co.y=-10.4
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='SOLID';area.spaces.active.shading.color_type='TEXTURE'
path=ROOT/'assets/blender/street-rebuilt-v17-manifest.json';manifest=json.loads(path.read_text())
for b in manifest['buildings']:
    if b['name'] in ('Wreake Valley Flooring','Syston Dry Cleaners','Nail and Spa shop'):b['eaves']={'Wreake Valley Flooring':9.5,'Syston Dry Cleaners':9.6,'Nail and Spa shop':9.2}[b['name']]
manifest['review_refinements']='Roof heights aligned to enlarged pub; street cameras corrected; procedural brick coursing for Blender review'
manifest['limitations'].append('Procedural brick shader must be baked/replaced for BO3; it is not an engine material')
path.write_text(json.dumps(manifest,indent=2)+'\n')
scene['v17_review_refined']=True
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/blender/pharmacie-street-rebuilt-v17.blend'))
result={'saved':bpy.data.filepath,'default_camera':scene.camera.name,'roof_height_corrected':True}
