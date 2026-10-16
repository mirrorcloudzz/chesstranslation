"""Read-only dependency and local tool checks. Does not run project pipelines."""
import importlib
import json
from pathlib import Path
import subprocess
import sys

from project_paths import ROOT, find_pdftoppm, resolve_project_path


def main():
    checks = {}
    for name in ['PIL', 'numpy', 'pypdf', 'reportlab', 'pdfplumber', 'chess', 'cv2', 'rapidocr_onnxruntime',
                 'winrt.windows.foundation', 'winrt.windows.foundation.collections', 'winrt.windows.globalization',
                 'winrt.windows.graphics.imaging', 'winrt.windows.media.ocr', 'winrt.windows.storage',
                 'winrt.windows.storage.streams']:
        try:
            module = importlib.import_module(name)
            checks[name] = {'ok': True, 'version': getattr(module, '__version__', None)}
        except Exception as exc:
            checks[name] = {'ok': False, 'error': str(exc)}
    try:
        exe = find_pdftoppm()
        subprocess.run([exe, '-v'], check=True, capture_output=True)
        checks['poppler'] = {'ok': True, 'path': exe}
    except Exception as exc:
        checks['poppler'] = {'ok': False, 'error': str(exc)}
    try:
        # Importing the builder registers all five existing proof fonts, but never builds a PDF.
        sys.path.insert(0, str(ROOT / 'tools/art_of_attack'))
        importlib.import_module('build_opening_proofs')
        checks['proof_fonts'] = {'ok': True}
        from prepare_art_of_attack import source_pdf
        checks['original_pdf'] = {'ok': True, 'path': str(source_pdf())}
    except Exception as exc:
        checks['proof_fonts_and_source'] = {'ok': False, 'error': str(exc)}
    try:
        from winrt.windows.media.ocr import OcrEngine
        from winrt.windows.globalization import Language
        engine = OcrEngine.try_create_from_language(Language('en-US'))
        checks['windows_ocr_en_US'] = {'ok': engine is not None}
    except Exception as exc:
        checks['windows_ocr_en_US'] = {'ok': False, 'error': str(exc)}
    try:
        from rapidocr_onnxruntime import RapidOCR
        import numpy as np
        engine = RapidOCR(intra_op_num_threads=1, inter_op_num_threads=1)
        engine(np.full((64, 256, 3), 255, dtype=np.uint8), use_cls=False)
        checks['rapidocr_inference'] = {'ok': True, 'scope': 'blank synthetic image only'}
    except Exception as exc:
        checks['rapidocr_inference'] = {'ok': False, 'error': str(exc)}
    for manifest in (ROOT / 'translations/art_of_attack/translation').glob('proof_manifest*.json'):
        missing = [str(resolve_project_path(row['path'])) for row in json.loads(manifest.read_text(encoding='utf-8'))
                   if not resolve_project_path(row['path']).is_file()]
        checks[manifest.name] = {'ok': not missing, 'missing': missing}
    print(json.dumps({'python': sys.executable, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if all(item['ok'] for item in checks.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
