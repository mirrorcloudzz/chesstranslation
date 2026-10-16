"""Read-only workspace audit; optionally save a reproducible file inventory."""
import argparse
import ast
from collections import Counter
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.md', '.txt', '.json', '.py', '.ps1', '.html', '.css', '.js', '.toml', '.yaml', '.yml', '.csv', '.tsv', '.xml', '.svg'}


def audit():
    result = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT, check=True, capture_output=True)
    names = sorted(set(result.stdout.decode('utf-8').split('\0')) - {''})
    rows, errors, json_count, text_count = [], [], 0, 0
    groups = Counter()
    for name in names:
        # Generated audit files are excluded so subsequent runs remain stable.
        if name.startswith('docs/inventory/'):
            continue
        path = ROOT / name
        if not path.is_file():
            errors.append({'file': name, 'error': 'missing file'})
            continue
        data = path.read_bytes()
        ext = path.suffix.lower()
        groups[name.split('/')[0]] += 1
        row = {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'kind': ext or 'config'}
        if ext in TEXT or path.name in {'.gitignore', '.gitattributes'}:
            try:
                content = data.decode('utf-8-sig')
                text_count += 1
                row['lines'] = len(content.splitlines())
                if ext == '.json':
                    json.loads(content)
                    json_count += 1
                if ext == '.py':
                    ast.parse(content, filename=name)
            except (UnicodeError, ValueError, SyntaxError) as exc:
                errors.append({'file': name, 'error': str(exc)})
        rows.append(row)
    expected = {
        'Chess Middlegame Planning (Peter Romanovsky) (Z-Library).pdf': '119cd5831d67838d9cb9e8d712215c3a54b46656f04798d3e81f4c58071b4072',
        'Logical Chess Move By Move Every Move explained (Irving Chernev) (Z-Library).pdf': '2c8355853d3bf078726e3a2d12eb63b687387f437ec1ed2f42518327f81aaed1',
        'How to think in chess (Przewoznik Soszynski) (Z-Library).pdf': 'c0436a76283af20b75856ef484d40999c74e5e0967bc20d88c9aa375e15e7b3c',
        'Art of Attack in Chess (Vladimir Vukovic) (z-library.sk, 1lib.sk, z-lib.sk).pdf': '888016578278b4b822afbf47600c601b61c4d9958dab0fdbc89280ded83d511a',
    }
    hashes = {r['path']: r['sha256'] for r in rows}
    originals = {n: hashes.get('books/originals/' + n) == h for n, h in expected.items()}
    for name, ok in originals.items():
        if not ok:
            errors.append({'file': 'books/originals/' + name, 'error': 'original checksum mismatch or missing'})
    base = ROOT / 'translations/art_of_attack'
    coverage = {}
    for folder, suffix in [('source_pages', 'png'), ('ocr/raw', 'json')]:
        missing = [n for n in range(1, 353) if not (base / folder / f'page-{n:03}.{suffix}').is_file()]
        coverage[folder] = {'expected': 352, 'missing': missing}
        if missing:
            errors.append({'file': str(base / folder), 'error': f'missing pages: {missing}'})
    manifest = json.loads((base / 'figures/manifest.json').read_text(encoding='utf-8'))
    missing_figures = [f['image'] for f in manifest if not (base / f['image']).is_file()]
    if missing_figures:
        errors.append({'file': 'figures/manifest.json', 'error': missing_figures})
    deps = {m: importlib.util.find_spec(m) is not None for m in ['PIL', 'numpy', 'pypdf', 'reportlab', 'pdfplumber', 'chess', 'cv2']}
    summary = dict(files=len(rows), bytes=sum(r['bytes'] for r in rows), directories=dict(groups), text_files_read=text_count,
                   json_files_parsed=json_count, originals_sha256_match=originals, art_of_attack_pages=coverage,
                   figures=len(manifest), missing_figures=missing_figures, python=sys.version.split()[0], dependencies=deps, errors=errors,
                   scope='Git tracked and non-ignored untracked files; excludes .git, ignored runtimes and docs/inventory. Binary files are hashed, not visually reviewed. Existing QA reports are not rerun.')
    return rows, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write docs/inventory/files.csv and audit.json only')
    args = parser.parse_args()
    rows, summary = audit()
    if args.write:
        dest = ROOT / 'docs/inventory'
        dest.mkdir(parents=True, exist_ok=True)
        stream = io.StringIO(newline='')
        writer = csv.DictWriter(stream, lineterminator=chr(10), fieldnames=['path', 'bytes', 'sha256', 'kind', 'lines'])
        writer.writeheader()
        writer.writerows(rows)
        (dest / 'files.csv').write_text(stream.getvalue(), encoding='utf-8-sig')
        (dest / 'audit.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary['errors'] else 0


if __name__ == '__main__':
    sys.exit(main())
