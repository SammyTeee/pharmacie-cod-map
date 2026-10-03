from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_downstairs_v14.py').read_text().replace('video-downstairs-v14.png','video-downstairs-v15.png')
exec(compile(code,__file__,'exec'))
code=(ROOT/'scripts/preview_video_interior.py').read_text().replace("'02 First floor - mapped rooms'","'05 Interior - photo-led dressing'").replace('(8.0,9.5,6.7)','(4.8,4.4,2.5)').replace('(-.5,17.2,5.8)','(9.9,10,2.6)').replace('((2,11),(7,15),(1,19))','((3,6),(7,11),(1,16))').replace('(x,y,8.1)','(x,y,3.9)').replace('data.energy=150','data.energy=250').replace('video-upstairs-v09.png','video-right-displays-v15.png')
exec(compile(code,__file__,'exec'))
