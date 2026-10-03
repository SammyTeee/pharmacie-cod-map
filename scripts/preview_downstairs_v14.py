from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
code=(ROOT/'scripts/preview_video_interior.py').read_text()
code=code.replace("'02 First floor - mapped rooms'","'05 Interior - photo-led dressing'").replace('(8.0,9.5,6.7)','(5.2,3.4,2.8)').replace('(-.5,17.2,5.8)','(2.8,15.8,1.65)').replace('((2,11),(7,15),(1,19))','((3,6),(7,11),(1,16))').replace('(x,y,8.1)','(x,y,3.9)').replace('data.energy=150','data.energy=250').replace('video-upstairs-v09.png','video-downstairs-v14.png')
exec(compile(code,__file__,'exec'))
