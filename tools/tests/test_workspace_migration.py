"""Regression checks use temporary fixtures and never run translation/PDF builders."""
import ast
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tools/art_of_attack'))
import prepare_art_of_attack as prepare
from project_paths import find_pdftoppm, resolve_project_path


class MigrationTests(unittest.TestCase):
    def test_archived_source_and_explicit_import(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            archive, supplied = folder/'archive.pdf', folder/'import.pdf'
            supplied.write_bytes(b'test original')
            digest = hashlib.sha256(supplied.read_bytes()).hexdigest()
            with patch.object(prepare, 'ARCHIVE', archive), patch.object(prepare, 'EXPECTED_SHA256', digest):
                with self.assertRaises(FileNotFoundError):prepare.source_pdf()
                self.assertEqual(prepare.source_pdf(supplied), supplied)
                archive.write_bytes(supplied.read_bytes())
                self.assertEqual(prepare.source_pdf(), archive)
                supplied.write_bytes(b'wrong book')
                with self.assertRaises(ValueError):prepare.source_pdf(supplied)
                with self.assertRaises(FileNotFoundError):prepare.source_pdf(folder/'missing.pdf')
                archive.write_bytes(b'corrupt archive')
                with self.assertRaises(ValueError):prepare.source_pdf()

    def test_export_preserves_readme_in_both_entry_points(self):
        for relative in ['tools/art_of_attack/export_art_of_attack.py', 'tmp/pdfs/export_art_of_attack.py']:
            with self.subTest(entry=relative), tempfile.TemporaryDirectory() as directory:
                spec = importlib.util.spec_from_file_location('fixture_export', ROOT/relative)
                export = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(export)
                base = Path(directory)
                for folder in ['figures', 'ocr/raw', 'ocr/chapters', 'qa']:(base/folder).mkdir(parents=True, exist_ok=True)
                (base/'figures/manifest.json').write_text('[]', encoding='utf-8')
                (base/'source_manifest.json').write_text(json.dumps({'pages': [{}]}), encoding='utf-8')
                archive = base/'fixture-source.bin'
                archive.write_bytes(b'fixture')
                readme = base/'README.md'
                original = b'\xef\xbb\xbf# User maintained\r\nChinese progress and corrections\r\n'
                readme.write_bytes(original)
                with patch.object(export, 'BASE', base), patch.object(export, 'ARCHIVE', archive), redirect_stdout(io.StringIO()):
                    export.main()
                    export.main()
                self.assertEqual(readme.read_bytes(), original)
                readme.unlink()
                self.assertTrue(export.ensure_readme(base))
                created = readme.read_bytes()
                self.assertFalse(export.ensure_readme(base))
                self.assertEqual(readme.read_bytes(), created)

    def test_legacy_manifest_paths_resolve_without_rewriting(self):
        for value in ['output/pdf/example.pdf', 'C:/Users/12059/Documents/Codex/chess/output/pdf/example.pdf',
                      r'C:\Users\12059\Documents\Codex\chess\output\pdf\example.pdf']:
            self.assertEqual(resolve_project_path(value), ROOT/'output/pdf/example.pdf')

    def test_poppler_override_is_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            exe=Path(directory)/'pdftoppm.exe'
            with patch.dict('os.environ', {'CHESS_PDFTOPPM': str(exe)}):
                with self.assertRaises(FileNotFoundError):find_pdftoppm()
                exe.touch()
                self.assertEqual(find_pdftoppm(), str(exe))

    def test_migrated_path_expressions_use_workspace_root(self):
        checked=0
        for folder in ['tools', 'tmp/pdfs']:
            for script in (ROOT/folder).rglob('*.py'):
                if 'tests' in script.parts:continue
                source=script.read_text(encoding='utf-8-sig')
                for node in ast.walk(ast.parse(source)):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id=='str':
                        expression=ast.get_source_segment(source,node)
                        if expression.startswith('str(Path(__file__).resolve().parents['):
                            result=Path(eval(compile(ast.Expression(node), str(script), 'eval'), {'Path':Path,'__file__':str(script)}))
                            self.assertTrue(result==ROOT or ROOT in result.parents, (script,result))
                            self.assertNotIn('tmp/tools', result.as_posix())
                            checked+=1
        self.assertGreater(checked,50)


if __name__=='__main__':unittest.main()
