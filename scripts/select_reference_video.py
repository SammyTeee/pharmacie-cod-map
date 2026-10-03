"""Select useful authentic frames from the reviewed video overview."""
import review_reference_video as review
import json
from PIL import Image, ImageDraw

selections = [(370,'Medicine cases and sofa'),(390,'Instrument display wall'),
 (430,'Front entrance from inside'),(460,'Skeleton display'),
 (490,'Bar and left passage'),(520,'Counter and pumps'),
 (620,'Rear corridor'),(632,'Stair flight'),(640,'Stair turn and window'),
 (652,'Upstairs room'),(660,'Upstairs seating'),(690,'Darts and bookcase'),
 (730,'Upstairs television wall'),(760,'Mirror and wall decoration'),
 (780,'Upstairs perimeter seating'),(800,'Upstairs wide view'),
 (810,'Piano and vintage radios'),(822,'Stair return view'),
 (850,'Rear passage signs'),(880,'Downstairs room towards front')]
frames=[]
canvas=Image.new('RGB',(1600,5*250+50),'#181b20');draw=ImageDraw.Draw(canvas)
draw.text((12,12),'Pharmacie reference tour | Blue Van Man | May 2019 | authentic video frames',fill='white')
for i,(second,label) in enumerate(selections):
    frame=review.extract(second);frame['observation']=label;frames.append(frame)
    with Image.open(review.ROOT/frame['file']) as original:
        thumb=original.copy();thumb.thumbnail((392,221))
        x=(i%4)*400+4;y=(i//4)*250+40;canvas.paste(thumb,(x,y))
        draw.text((x,y+223),frame['time']+'  '+label,fill='white')
canvas.save(review.OUT/'selected-tour.jpg',quality=94)
(review.OUT/'selected-manifest.json').write_text(json.dumps({'source_url':review.info['webpage_url'],
 'status':'Historical reference; compare with newer photos and user corrections',
 'frames':frames},indent=2)+'\n',encoding='utf-8')
print('Selected 20 frames and wrote selected-tour.jpg')
