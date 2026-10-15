from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
SRC=ROOT/'tmp/pdfs/middlegame_chapters34/source'
files=[SRC/f'page-{p:03d}.png' for p in range(101,145)]
for batch in range(0,len(files),12):
    sheet=Image.new('RGB',(1200,1600),'#ccc'); d=ImageDraw.Draw(sheet)
    for j,path in enumerate(files[batch:batch+12]):
        im=Image.open(path).convert('RGB'); im.thumbnail((285,370))
        x=(j%4)*300; y=(j//4)*530
        sheet.paste(im,(x,y+25)); d.text((x+5,y+5),path.stem,fill='black')
    sheet.save(ROOT/f'tmp/pdfs/middlegame_chapters34/ch4sources{batch//12+1}.jpg')
