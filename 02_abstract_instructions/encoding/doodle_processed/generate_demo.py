
import base64,io,json,subprocess
from PIL import Image,ImageDraw
bits='10010000110010101101100011011000110111'
assert len(bits)==38
sequence='0'+bits+'1'
im=Image.new('RGB',(1390,360),'white')
d=ImageDraw.Draw(im)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1390" height="360" viewBox="0 0 1390 360">','<rect width="1390" height="360" fill="white"/>','<g fill="none" stroke="black" stroke-width="4" stroke-linejoin="round">']
def line(points):
 d.line(points,fill='black',width=4)
 svg.append('<polyline points="'+' '.join(str(x)+','+str(y) for x,y in points)+'"/>')
previous=(18,100)
for i,bit in enumerate(sequence):
 row,col=divmod(i,20)
 cx=60+(col if row==0 else 19-col)*64
 cy=100 if row==0 else 260
 entry=(cx-20,cy) if row==0 else (cx+20,cy)
 exit=(cx+20,cy) if row==0 else (cx-20,cy)
 if i==20:
  line([previous,(1335,100),(1335,260),entry])
 else:
  line([previous,entry])
 d.ellipse((cx-20,cy-26,cx+20,cy+26),outline='black',width=4)
 svg.append('<ellipse cx="'+str(cx)+'" cy="'+str(cy)+'" rx="20" ry="26"/>')
 if bit=='1':
  line([(cx-20,cy),(cx+20,cy)])
 previous=exit
line([previous,(18,260)])
svg.extend(['</g>','</svg>'])
svg_text='\n'.join(svg)

from pathlib import Path
root=Path(__file__).resolve().parent
im.save(root/'doodle_redrawn.png')
(root/'doodle_redrawn.svg').write_text(svg_text,encoding='utf-8')
