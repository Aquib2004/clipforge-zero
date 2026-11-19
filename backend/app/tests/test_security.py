"""Security tests: URL validation and path traversal protection."""

import pytest

from app.core.security import SecurityError, is_safe_url, is_youtube_url, safe_workspace_path


def test_is_safe_url_http():
    assert is_safe_url("https://www.youtube.com/watch?v=abc") is True
    assert is_safe_url("http://example.com") is True


def test_is_safe_url_rejects_file_scheme():
    assert is_safe_url("file:///etc/passwd") is False


def test_is_safe_url_rejects_localhost():
    assert is_safe_url("http://localhost/") is False
    assert is_safe_url("http://127.0.0.1/") is False


def test_is_safe_url_rejects_malformed():
    assert is_safe_url("not-a-url") is False
    assert is_safe_url("") is False


def test_is_youtube_url():
    assert is_youtube_url("https://www.youtube.com/watch?v=abc") is True
    assert is_youtube_url("https://youtu.be/abc") is True
    assert is_youtube_url("https://evil.com/video") is False
    assert is_youtube_url("../../etc/passwd") is False


def test_safe_workspace_path_traversal(tmp_path):

    base = tmp_path / "workspace"
    base.mkdir()

    # Normal path works
    result = safe_workspace_path(base, "projects", "proj-1")
    assert result == base / "projects" / "proj-1"

    # Traversal attempt raises
    with pytest.raises(SecurityError):
        safe_workspace_path(base, "..", "escape")
