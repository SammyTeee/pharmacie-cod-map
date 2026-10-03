"""Render opposite-street photo scenery from pub pavement; clean temporary state."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_video_interior.py').read_text()
code=code.replace("'02 First floor - mapped rooms'","'03 Both floors - assembled exterior'")
code=code.replace('(8.0,9.5,6.7)','(5.0,-1.2,3.9)').replace('(-.5,17.2,5.8)','(4.0,-13,3.8)').replace('camdata.lens=24','camdata.lens=16')
code=code.replace('((2,11),(7,15),(1,19))','((-8,-8),(8,-8),(22,-8))').replace('(x,y,8.1)','(x,y,11)').replace('data.energy=150','data.energy=1700')
code=code.replace("(.2,.18,.14,1)","(.5,.58,.7,1)").replace("default_value=.35","default_value=.65")
code=code.replace('video-upstairs-v09.png','street-photo-fronts-v11.png')
exec(compile(code,__file__,'exec'))
result={'preview':'assets/blender/street-photo-fronts-v11.png'}
