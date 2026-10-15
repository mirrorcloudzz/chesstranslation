from PIL import Image
import numpy as np
ROOT='tmp/pdfs/middlegame_chapters34/source'
for p in [102,103,104,105]:
 a=np.array(Image.open(f'{ROOT}/page-{p:03d}.png').convert('L')); hits=[]
 for y,row in enumerate(a):
  ids=np.where(row<90)[0]
  if len(ids):
   for g in np.split(ids,np.where(np.diff(ids)>5)[0]+1):
    if 300<len(g)<800:hits.append((y,int(g[0]),int(g[-1])))
 print(p,a.shape,hits[:8])
