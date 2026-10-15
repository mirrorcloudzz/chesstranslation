from pathlib import Path
import numpy as np
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'tmp/pdfs/middlegame_chapters34/source'; OUT=ROOT/'translations/chess_middlegame_planning/chapter_four_figures'
OUT.mkdir(exist_ok=True)
def runs(row,threshold=90,minlen=300,gap=5):
    xs=np.flatnonzero(row<threshold)
    if not len(xs): return []
    out=[]; start=prev=int(xs[0])
    for x in map(int,xs[1:]):
        if x-prev<=gap: prev=x; continue
        if prev-start+1>=minlen: out.append((start,prev))
        start=prev=x
    if prev-start+1>=minlen: out.append((start,prev))
    if prev-start+1>=minlen: out.append((start,prev))
    return out
def group(lines):
    gs=[]
    for y,x1,x2 in lines:
        if gs and y-gs[-1][-1][0]<=9 and abs(x1-gs[-1][-1][1])<30 and abs(x2-gs[-1][-1][2])<30: gs[-1].append((y,x1,x2))
        else: gs.append([(y,x1,x2)])
    return [(round(sum(a for a,_,_ in g)/len(g)),round(sum(b for _,b,_ in g)/len(g)),round(sum(c for _,_,c in g)/len(g))) for g in gs]
manifest=[]
for page in range(101,145):
 im=Image.open(SRC/f'page-{page:03d}.png').convert('L'); ar=np.asarray(im); lines=[]
 for y,row in enumerate(ar):
  lines += [(y,a,b) for a,b in runs(row) if 300<=b-a+1<=700]
 gr=group(lines); boxes=[]
 for idx,(ty,x1,x2) in enumerate(gr):
  w=x2-x1+1
  for by,bx1,bx2 in gr[idx+1:]:
   h=by-ty
   if h<300: continue
   if h>750: break
   if abs(x1-bx1)<40 and abs(x2-bx2)<40 and abs(h-(w+bx2-bx1+1)/2)<60:
    box=(min(x1,bx1),ty,max(x2,bx2),by)
    if not any(sum(abs(a-b) for a,b in zip(box,old))<60 for old in boxes): boxes.append(box)
    break
 for n,(x1,y1,x2,y2) in enumerate(boxes,1):
  crop=ImageOps.autocontrast(im.crop((max(0,x1-8),max(0,y1-8),min(im.width,x2+9),min(im.height,y2+9))))
  name=f'page-{page:03d}-diagram-{n}.png'; crop.save(OUT/name); manifest.append((page,n,name,(x1,y1,x2,y2)))
print('boards',len(manifest),manifest)
for batch in range(0,len(manifest),16):
 sheet=Image.new('RGB',(1200,1800),'#ddd'); d=ImageDraw.Draw(sheet)
 for k,(pg,n,name,box) in enumerate(manifest[batch:batch+16]):
  im=Image.open(OUT/name).convert('RGB'); im.thumbnail((290,410)); x=k%4*300;y=k//4*450
  sheet.paste(im,(x,y+25));d.text((x+5,y+5),f'{pg}-{n}',fill='black')
 sheet.save(ROOT/f'tmp/pdfs/middlegame_chapters34/ch4boards{batch//16+1}.jpg')
