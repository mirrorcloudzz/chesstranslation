import sys,json,hashlib,shutil,time,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/ocrdeps'))
from PIL import Image,ImageDraw,ImageOps
import numpy as np
import cv2
from pypdf import PdfReader
BASE=ROOT/'translations/art_of_attack'
SOURCE=Path('C:/Users/12059/Downloads/Art of Attack in Chess (Vladimir Vukovic) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
ARCHIVE=ROOT/'books/originals'/SOURCE.name
SECTIONS=[('front','Cover and publication details',1,2),('contents','Contents',3,3),('symbols','Symbols',4,4),('preface','Preface by John Nunn',5,5),('introduction','Introduction',6,13),('ch01','The attack against the uncastled king',14,27),('ch02','The attack on the king that has lost the right to castle',28,50),('ch03','On castling and attacking the castled position in general',51,65),('ch04','Mating patterns',66,79),('ch05','Focal-points',80,120),('ch06','The classic bishop sacrifice',121,141),('ch07','Ranks, files, and diagonals in the attack on the castled king',142,182),('ch08','Pieces and pawns in the attack on the castled king',183,230),('ch09','The attack on the fianchettoed and queenside castling positions',231,246),('ch10','Defending against the attack on the castled king',247,292),('ch11','The phases of the attack on the castled king',293,333),('ch12','The attack on the king as an integral part of the game',334,349),('players','Index of Players',350,351),('openings','Index of Openings',352,352)]
def section(n):return next(s for s in SECTIONS if s[2]<=n<=s[3])
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def extract():
    for d in ['source_pages','ocr/raw','ocr/chapters','figures','qa']:(BASE/d).mkdir(parents=True,exist_ok=True)
    if not ARCHIVE.exists():shutil.copy2(SOURCE,ARCHIVE)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(SOURCE)==sha(ARCHIVE)
    reader=PdfReader(ARCHIVE);pages=[]
    for n,p in enumerate(reader.pages,1):
        assert len(p.images)==1,(n,len(p.images))
        image=p.images[0].image
        rotation=int(p.get('/Rotate',0))%360
        if rotation:image=image.rotate(-rotation,expand=True)
        dest=BASE/'source_pages'/f'page-{n:03}.png'
        image.save(dest)
        pages.append(dict(pdf_page=n,printed_page=n if n>=3 else None,section=section(n)[0],width=image.width,height=image.height,pdf_rotation_applied=rotation,file=str(dest.relative_to(BASE))))
    save(BASE/'source_manifest.json',dict(source_name=SOURCE.name,sha256=sha(ARCHIVE),pages=pages,date='2026-09-30',note='Original embedded page bitmaps preserved without resampling, with PDF page rotation applied. Print/PDF page correspondence to be checked at TOC boundaries.'))
    save(BASE/'contents.json',[dict(id=k,title=t,pdf_start=a,pdf_end=b,print_start=a if a>=3 else None,print_end=b if a>=3 else None) for k,t,a,b in SECTIONS])
    print('Saved',len(pages),'original page images',flush=True)

def find_boards(im):
    a=np.array(im.convert('L'));h,w=a.shape
    bw=(a<150).astype('uint8')*255
    # Join small scan gaps without inventing board content; only detection uses this mask.
    mask=cv2.morphologyEx(bw,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8))
    contours,_=cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    boxes=[]
    for c in contours:
        x,y,cw,ch=cv2.boundingRect(c)
        if not(.25*w<cw<.50*w and .80<cw/ch<4.5 and ch>90 and y>70 and x>100 and x+cw<w-100):continue
        # A board's outer frame encloses almost the whole square.
        if cv2.contourArea(c)<.75*cw*ch:continue
        boxes.append((x,y,x+cw,y+ch))
    unique=[]
    for box in sorted(boxes,key=lambda b:-(b[2]-b[0])*(b[3]-b[1])):
        if any(abs(box[0]-b[0])+abs(box[1]-b[1])+abs(box[2]-b[2])+abs(box[3]-b[3])<120 for b in unique):continue
        if any(box[0]>=b[0]-10 and box[1]>=b[1]-10 and box[2]<=b[2]+10 and box[3]<=b[3]+10 for b in unique):continue
        unique.append(box)
    return sorted(unique,key=lambda b:(b[1],b[0]))

def crops():
    figures=[]
    # Manually inspected source coordinates, expressed on the 1311 x 1882 preview.
    additions={47:[(473,1237,884,1656)],66:[(540,1099,952,1317),(536,1480,948,1698)],67:[(453,448,865,663),(455,909,866,1122),(455,1293,866,1509)],68:[(470,1140,881,1355)],69:[(464,831,876,1046),(465,1292,876,1508)],70:[(543,220,956,434),(540,718,953,934),(535,1293,947,1510)],71:[(458,222,870,437)],72:[(579,216,991,434)],74:[(586,680,1000,896)],75:[(461,222,874,436)]}
    additions[72].append((574,674,987,892))
    for n in range(3,353):
        im=Image.open(BASE/'source_pages'/f'page-{n:03}.png')
        boxes=find_boards(im)
        boxes += [tuple(round(v*(im.width/1311 if i%2==0 else im.height/1882)) for i,v in enumerate(b)) for b in additions.get(n,[])]
        for j,box in enumerate(sorted(boxes,key=lambda b:(b[1],b[0])),1):
            x,y,r,b=box
            # Preserve the W/B side-to-move indicator printed to the left.
            crop=(max(0,x-100),max(0,y-10),min(im.width,r+12),min(im.height,b+12))
            sid=section(n)[0];dest=BASE/'figures'/sid;dest.mkdir(exist_ok=True)
            name=f'AA-p{n:03}-fig{j:02}.png';im.crop(crop).save(dest/name)
            figures.append(dict(id=f'AA-p{n:03}-fig{j:02}',pdf_page=n,printed_page=n,section=sid,board_bbox=list(box),crop_bbox=list(crop),image=str((dest/name).relative_to(BASE)),caption='',position_status='pending_context_review',crop_status='page_contact_sheet_checked',partial_board=(b-y)<.8*(r-x)))
    save(BASE/'figures/manifest.json',figures)
    print('Cropped',len(figures),'board candidates',flush=True)
    for start in range(0,len(figures),30):
        sheet=Image.new('RGB',(1500,1800),'#ddd');draw=ImageDraw.Draw(sheet)
        for j,f in enumerate(figures[start:start+30]):
            im=Image.open(BASE/f['image']).convert('RGB');im.thumbnail((290,270))
            x=(j%5)*300;y=(j//5)*300
            sheet.paste(im,(x,y+25));draw.text((x+5,y+5),f['id'],fill='black')
        sheet.save(BASE/'qa'/f'boards-{start+1:03}.jpg',quality=88)
    # Complete-page contact sheets, to detect missing boards and layout variants.
    for start in range(1,353,24):
        sheet=Image.new('RGB',(1500,2160),'#ddd');d=ImageDraw.Draw(sheet)
        for j,n in enumerate(range(start,min(353,start+24))):
            im=Image.open(BASE/'source_pages'/f'page-{n:03}.png').convert('RGB');im.thumbnail((245,330))
            x=j%6*250;y=j//6*540
            sheet.paste(im,(x,y+25));d.text((x+5,y+5),str(n),fill='black')
            for f in [f for f in figures if f['pdf_page']==n]:
                scale=im.width/Image.open(BASE/'source_pages'/f'page-{n:03}.png').width
                a,b,c,e=f['board_bbox'];d.rectangle((x+a*scale,y+25+b*scale,x+c*scale,y+25+e*scale),outline='red',width=2)
        sheet.save(BASE/'qa'/f'pages-{start:03}.jpg',quality=88)

def ocr_page(engine,n):
    out=BASE/'ocr/raw'/f'page-{n:03}.json'
    if out.exists():return
    im=Image.open(BASE/'source_pages'/f'page-{n:03}.png').convert('RGB')
    result,_=engine(np.array(im),use_cls=False)
    rows=[]
    for box,text,score in result or []:
        xs=[p[0] for p in box];ys=[p[1] for p in box]
        rows.append(dict(bbox=[round(min(xs),1),round(min(ys),1),round(max(xs),1),round(max(ys),1)],text=text,confidence=round(float(score),4)))
    save(out,dict(pdf_page=n,printed_page=n if n>=3 else None,width=im.width,height=im.height,engine='RapidOCR PP-OCRv4',status='raw_ocr_not_manually_proofread',lines=rows))
    print('OCR',n,len(rows),'lines',flush=True)

def ocr(start,end,step):
    from rapidocr_onnxruntime import RapidOCR
    engine=RapidOCR(intra_op_num_threads=1,inter_op_num_threads=1,det_limit_side_len=1200)
    for n in range(start,end+1,step):ocr_page(engine,n)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['extract','crops','ocr']);p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=352);p.add_argument('--step',type=int,default=1);a=p.parse_args()
    if a.mode=='extract':extract()
    elif a.mode=='crops':crops()
    else:ocr(a.start,a.end,a.step)
