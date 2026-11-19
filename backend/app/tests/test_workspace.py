"""Workspace path tests."""

from app.core.paths import data_dir, ensure_workspace


def test_ensure_workspace_creates_dirs(tmp_path, monkeypatch):
    import app.core.paths as paths_module

    monkeypatch.setattr(paths_module, "workspace_root", lambda: tmp_path)
    monkeypatch.setattr(paths_module, "data_dir", lambda: tmp_path / "data")

    ensure_workspace()
    assert (tmp_path / "data").exists()
    assert (tmp_path / "data" / "projects").exists()


def test_data_dir_returns_path():
    d = data_dir()
    assert d is not None
    assert str(d).endswith("data") or "data" in str(d)
