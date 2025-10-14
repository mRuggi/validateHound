# core/loader.py
from pathlib import Path
import json
import zipfile
from typing import Dict, Any, Tuple, Iterable, Optional


class LoaderError(Exception):
    """Generic loader error."""
    pass


class JSONParseError(LoaderError):
    """Raised when a JSON file cannot be parsed."""
    def __init__(self, filename: str, original_exc: Exception):
        super().__init__(f"Failed to parse JSON file {filename}: {original_exc}")
        self.filename = filename
        self.original_exc = original_exc


class UnsupportedInputError(LoaderError):
    """Raised when the provided path is neither a directory nor a zip."""
    pass


def _iter_json_files_in_dir(path: Path) -> Iterable[Path]:
    for p in sorted(path.iterdir()):
        if p.is_file() and p.suffix.lower() == ".json":
            yield p


def _read_json_file(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as e:
        raise JSONParseError(str(path), e)

    # RustHound CE normalization
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        data = data["data"]

    return data

def _read_json_bytes(name: str, bts: bytes) -> Any:
    try:
        data = json.loads(bts.decode("utf-8"))
    except Exception as e:
        raise JSONParseError(name, e)

    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        data = data["data"]

    return data

def load_from_dir(path: Path) -> Dict[str, Any]:
    """
    Read all .json files from a directory and return a dict mapping filename -> parsed JSON.
    """
    if not path.exists() or not path.is_dir():
        raise LoaderError(f"Path {path} is not an existing directory")

    out: Dict[str, Any] = {}
    for p in _iter_json_files_in_dir(path):
        out[p.name] = _read_json_file(p)
    return out


def load_from_zip(path: Path) -> Dict[str, Any]:
    """
    Read all .json files from a zip archive and return a dict mapping filename -> parsed JSON.
    """
    if not path.exists() or not path.is_file():
        raise LoaderError(f"ZIP file {path} does not exist")

    out: Dict[str, Any] = {}
    try:
        with zipfile.ZipFile(path, "r") as z:
            # list and sort for deterministic ordering
            for name in sorted(z.namelist()):
                if name.lower().endswith(".json"):
                    try:
                        raw = z.read(name)
                    except Exception as e:
                        raise LoaderError(f"Failed to read {name} from zip: {e}")
                    out[Path(name).name] = _read_json_bytes(name, raw)
    except zipfile.BadZipFile as e:
        raise LoaderError(f"Invalid zip file {path}: {e}")
    return out


def load(path: Path) -> Dict[str, Any]:
    """
    Generic loader: accepts a directory or a .zip file and returns parsed JSON files.
    Raises LoaderError / JSONParseError on failures.
    """
    if not isinstance(path, Path):
        path = Path(path)

    if path.is_dir():
        return load_from_dir(path)
    if path.is_file() and path.suffix.lower() == ".zip":
        return load_from_zip(path)
    raise UnsupportedInputError("Input must be a directory or a .zip file")
