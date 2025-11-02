import io
import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

def make_file(size, content_type="image/png"):
    data = io.BytesIO(b"x" * size)
    data.name = "test.png"
    return data, content_type

def test_upload_png(tmp_path, monkeypatch):
    tmp_uploads = tmp_path / "uploads"
    tmp_uploads.mkdir()
    monkeypatch.setattr("app.api.routes.media.UPLOAD_DIR", tmp_uploads)

    data, mime = make_file(1024)
    resp = client.post(
        "/media/",
        files={"file": ("pic.png", data.getvalue(), mime)},
    )
    assert resp.status_code == 200
    assert resp.json()["mime_type"] == "image/png"

def test_reject_large_file():
    data, mime = make_file(11 * 1024 * 1024)
    resp = client.post(
        "/media/",
        files={"file": ("big.png", data.getvalue(), mime)},
    )
    assert resp.status_code == 413

def test_reject_bad_type():
    data, mime = make_file(1024, "image/gif")
    resp = client.post(
        "/media/",
        files={"file": ("bad.gif", data.getvalue(), mime)},
    )
    assert resp.status_code == 415