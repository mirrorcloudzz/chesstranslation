import sys,asyncio,time,argparse
from prepare_art_of_attack import BASE,save
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.globalization import Language
from winrt.windows.storage import StorageFile,FileAccessMode
from winrt.windows.graphics.imaging import BitmapDecoder

async def main(a):
    engine=OcrEngine.try_create_from_language(Language('en-US'))
    out=BASE/a.output;out.mkdir(parents=True,exist_ok=True)
    for n in range(a.start,a.end+1):
        dest=out/f'page-{n:03}.json'
        if dest.exists():continue
        t=time.time()
        file=await StorageFile.get_file_from_path_async(str(BASE/'source_pages'/f'page-{n:03}.png'))
        stream=await file.open_async(FileAccessMode.READ)
        decoder=await BitmapDecoder.create_async(stream)
        bitmap=await decoder.get_software_bitmap_async()
        result=await engine.recognize_async(bitmap)
        lines=[]
        for line in result.lines:
            rects=[w.bounding_rect for w in line.words]
            lines.append(dict(text=line.text,bbox=[min(r.x for r in rects),min(r.y for r in rects),max(r.x+r.width for r in rects),max(r.y+r.height for r in rects)],confidence=None))
        data=dict(pdf_page=n,printed_page=n if n>=3 else None,width=bitmap.pixel_width,height=bitmap.pixel_height,engine='Windows OCR en-US',status='raw_ocr_not_manually_proofread',lines=lines)
        # Other OCR workers may have finished this page while Windows OCR ran.
        if not dest.exists():save(dest,data)
        bitmap.close();stream.close()
        print(f'OCR {n}: {len(lines)} lines, {time.time()-t:.2f}s',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',type=int,default=1);p.add_argument('--end',type=int,default=352);p.add_argument('--output',default='ocr/raw');a=p.parse_args()
    asyncio.run(main(a))
