"""Resolve machine-local tools without embedding a user's profile path."""
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def find_pdftoppm():
    override = os.environ.get('CHESS_PDFTOPPM')
    if override:
        candidate = Path(override).expanduser()
        if not candidate.is_file():
            raise FileNotFoundError(f'CHESS_PDFTOPPM does not exist: {candidate}')
        return str(candidate)
    installed = shutil.which('pdftoppm')
    if installed:
        return installed
    candidate = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
    if candidate.is_file():
        return str(candidate)
    raise FileNotFoundError('pdftoppm not found. Add Poppler to PATH or set CHESS_PDFTOPPM to its executable.')


def resolve_project_path(value):
    """Rebase archived proof manifests in memory; never rewrite historical JSON."""
    normalized = str(value).replace('\\', '/')
    old_root = 'C:/Users/12059/Documents/Codex/chess/'
    if normalized.startswith(old_root):
        return ROOT / normalized[len(old_root):]
    path = Path(normalized)
    return path if path.is_absolute() else ROOT / path
