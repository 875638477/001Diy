"""Render assembly review from actual b019 placement origins. Callouts are not native artwork glyphs."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021'
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',12);title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',25)
scale=18;ox=60;oy=1200
xy=lambda p:(round(ox+p[0]*scale),round(oy-p[1]*scale))
for v in ['2L','4L']:
 s=json.loads((H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING/normalized.json').read_text());im=Image.new('RGB',(1560,1320),'white');d=ImageDraw.Draw(im)
 d.text((45,25),f'{v} b019 assembly review - TRAINING_NOT_FOR_ASSEMBLY',font=title,fill='#a01818');d.text((45,60),'Actual CAD origins / mm / top view. Callouts are review labels, not native Cadence glyphs.',font=font,fill='#333333')
 outline=[[2,0],[78,0],[80,2],[80,58],[78,60],[2,60],[0,58],[0,2]];d.polygon([xy(p) for p in outline],fill='#fafafa',outline='#222222',width=2)
 for i in range(0,81,5):
  d.line([xy((i,0)),xy((i,60))],fill='#e6e6e6');d.text(xy((i,-1.5)),str(i),font=small,fill='#555')
 for i in range(0,61,5):
  d.line([xy((0,i)),xy((80,i))],fill='#e6e6e6');d.text((ox-27,xy((0,i))[1]-5),str(i),font=small,fill='#555')
 for p in s['placements']:
  b=p['bodyExtent'];color='#b45309' if p['ref'] in ['R12','R13'] else '#0d6791';d.rectangle([xy((b[0][0],b[1][1])),xy((b[1][0],b[0][1]))],outline=color,width=1)
  for q in p['pins']:
   if not q['number']:continue
   bb=q['padBBox'];d.rectangle([xy((bb[0][0],bb[1][1])),xy((bb[1][0],bb[0][1]))],fill='#d9bd67')
  cx,cy=xy(p['xy']);d.line([(cx-4,cy),(cx+4,cy)],fill='#bf1010');d.line([(cx,cy-4),(cx,cy+4)],fill='#bf1010')
  d.text((cx,cy),p['ref'],font=small,fill=color,anchor='mm',stroke_width=1,stroke_fill='white')
 for h in s['mechanicalPins']:
  cx,cy=xy(h['xy']);rad=h['drillDiameter']*scale/2;d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline='#222222',fill='white',width=2)
 d.text((60,1250),'Blue: footprint PlaceBound. Brown: R12/R13 DNP. Red: symbol origin. Six NPTH holes shown separately.',font=font,fill='#333333');d.text((60,1280),'BOM, all80 coordinates, THT/DNP exclusions and pin1 coordinates accompany this diagram. Factory mapping pending.',font=font,fill='#333333')
 im.save(J/f'assembly/assembly_review_{v}_b019_TRAINING.png')
print('Rendered 2 assembly review PNGs')
