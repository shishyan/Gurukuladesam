"""Collect the four newly generated scenes of each song for visual review."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('batch',type=Path)
args = parser.parse_args()
root = args.batch.resolve()
jobs = json.loads((root/'jobs.json').read_text(encoding='utf-8'))['songs']
review = Image.new('RGB',(1280,len(jobs)*210),'#151515')
draw = ImageDraw.Draw(review)
for row,job in enumerate(jobs):
    contact = Image.open(root/job['slug']/'contact.jpg').convert('RGB')
    for column,scene in enumerate([0,3,7,11]):
        x,y = (scene%4)*320,(scene//4)*210
        review.paste(contact.crop((x,y,x+320,y+180)),(column*320,row*210))
        draw.text((column*320+6,row*210+184),job['english']+f' / key scene {column+1}',fill='white')
review.save(root/'batch-review.jpg',quality=92)
print(root/'batch-review.jpg')
