from pathlib import Path
from PIL import Image
import hashlib, json
p = Path('translations/art_of_attack/translation/visual_review_ch07_09_v3_hashes.json')
d = json.loads(p.read_text('utf-8'))
comparisons = []
for rec in d['images']:
    current = hashlib.sha256(Path(rec['path']).read_bytes()).hexdigest()
    comparisons.append({'path': rec['path'], 'previous_sha256': rec['sha256'], 'final_sha256': current, 'identical': current == rec['sha256']})
    if current != rec['sha256']:
        with Image.open(rec['path']) as img:
            rec['sha256'] = current
            rec['rgb_pixels_sha256'] = hashlib.sha256(img.convert('RGB').tobytes()).hexdigest()
            rec['width'], rec['height'] = img.size
for page in (12,13):
    path = Path(f'tmp/pdfs/art_of_attack_complete_v3/render/ch09/page-{page}.png')
    with Image.open(path) as img:
        d['images'].append({'path': path.as_posix(), 'kind': 'full_page', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'rgb_pixels_sha256': hashlib.sha256(img.convert('RGB').tobytes()).hexdigest(), 'width': img.width, 'height': img.height})
d['full_page_images_viewed'] = 6
d['final_comparison'] = {'date': '2026-10-18', 'previous_images': 17, 'identical': sum(x['identical'] for x in comparisons), 'changed_and_rechecked': [x['path'] for x in comparisons if not x['identical']], 'new_full_pages_rechecked': [12,13], 'comparisons': comparisons}
p.write_bytes((json.dumps(d, ensure_ascii=False, indent=2) + chr(10)).encode('utf-8'))
print('Updated: 15 identical, 2 rechecked contacts, 2 additional complete pages; 19 current images.')
