# tests/test_loader.py
import json
import zipfile
import io
from pathlib import Path
import pytest
from validatehound.core import loader


SAMPLE_USERS = [
    {"objectid": "U1", "Name": "alice"},
    {"objectid": "U2", "Name": "bob"}
]

SAMPLE_GROUPS = [
    {"objectid": "G1", "Name": "Domain Admins", "Members": ["U1"]},
]


def _write_sample_dir(tmp_path: Path) -> Path:
    d = tmp_path / "sample_dir"
    d.mkdir()
    (d / "users.json").write_text(json.dumps(SAMPLE_USERS), encoding="utf-8")
    (d / "groups.json").write_text(json.dumps(SAMPLE_GROUPS), encoding="utf-8")
    # add a non-json file that must be ignored
    (d / "README.txt").write_text("ignore me", encoding="utf-8")
    return d


def _make_sample_zip_bytes() -> bytes:
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w") as z:
        z.writestr("users.json", json.dumps(SAMPLE_USERS).encode("utf-8"))
        z.writestr("groups.json", json.dumps(SAMPLE_GROUPS).encode("utf-8"))
        z.writestr("notes/README.txt", b"ignore")
    mem.seek(0)
    return mem.read()


def test_load_from_dir(tmp_path: Path):
    d = _write_sample_dir(tmp_path)
    out = loader.load_from_dir(d)
    assert "users.json" in out
    assert "groups.json" in out
    assert isinstance(out["users.json"], list)
    assert out["users.json"][0]["Name"] == "alice"


def test_load_from_zip(tmp_path: Path):
    zbytes = _make_sample_zip_bytes()
    zpath = tmp_path / "sample.zip"
    zpath.write_bytes(zbytes)
    out = loader.load_from_zip(zpath)
    assert "users.json" in out
    assert "groups.json" in out
    assert out["groups.json"][0]["Name"] == "Domain Admins"


def test_load_generic(tmp_path: Path):
    # directory path
    d = _write_sample_dir(tmp_path)
    out1 = loader.load(d)
    assert "users.json" in out1

    # zip path
    zbytes = _make_sample_zip_bytes()
    zpath = tmp_path / "sample.zip"
    zpath.write_bytes(zbytes)
    out2 = loader.load(zpath)
    assert "users.json" in out2


def test_invalid_json_in_zip(tmp_path: Path):
    # create a zip with invalid json
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w") as z:
        z.writestr("bad.json", b"{ not valid json }")
    mem.seek(0)
    zpath = tmp_path / "bad.zip"
    zpath.write_bytes(mem.read())
    with pytest.raises(loader.JSONParseError) as exc:
        loader.load_from_zip(zpath)
    assert "bad.json" in str(exc.value)


def test_invalid_input_type(tmp_path: Path):
    # passing a file that's not zip
    txt = tmp_path / "file.txt"
    txt.write_text("hello", encoding="utf-8")
    with pytest.raises(loader.UnsupportedInputError):
        loader.load(txt)
