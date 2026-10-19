from pathlib import Path
from PIL import Image
import hashlib, json

root = Path.cwd()
base = Path('tmp/pdfs/art_of_attack_complete_v3')
files = []
for chapter in ('ch07', 'ch08', 'ch09'):
    files.extend((p, 'contact') for p in sorted((base / 'contacts').glob(chapter + '-*.jpg')))
for chapter, page in [('ch07', 53), ('ch08', 10), ('ch08', 46), ('ch09', 10)]:
    files.append((base / 'render' / chapter / f'page-{page:02}.png', 'full_page'))
records = []
for path, kind in files:
    with Image.open(path) as img:
        rgb = img.convert('RGB')
        records.append({
            'path': path.as_posix(),
            'kind': kind,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'rgb_pixels_sha256': hashlib.sha256(rgb.tobytes()).hexdigest(),
            'width': img.width,
            'height': img.height,
        })
output = Path('translations/art_of_attack/translation/visual_review_ch07_09_v3_hashes.json')
data = {'review_date': '2026-10-18', 'scope': {'ch07': 57, 'ch08': 66, 'ch09': 20}, 'contact_images_viewed': 13, 'full_page_images_viewed': 4, 'images': records}
output.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + chr(10)).encode('utf-8'))
print(f'Saved {len(records)} viewed image hashes to {output}')
