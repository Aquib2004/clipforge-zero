"""Security primitives.

- URL validation (no shell, no local file paths passed as URLs)
- Workspace path traversal protection
- Safe subprocess wrapper (shell=False always)
"""

import subprocess
from pathlib import Path
from urllib.parse import urlparse


class SecurityError(ValueError):
    """Raised when an input violates a security policy."""


def is_safe_url(url: str) -> bool:
    """Return True if url is a well-formed http/https URL with a real host.

    Rejects:
    - non-http(s) schemes
    - missing hostnames
    - localhost / loopback hosts (used to block file://-style bypasses)
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.hostname:
        return False
    host = parsed.hostname.lower()
    # 0.0.0.0 is rejected here (not bound to) — noqa: S104
    if host in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):  # noqa: S104
        return False
    return True


ALLOWED_YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def is_youtube_url(url: str) -> bool:
    """Return True if url points to youtube.com or youtu.be."""
    if not is_safe_url(url):
        return False
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    host = (parsed.hostname or "").lower()
    if host in ALLOWED_YOUTUBE_DOMAINS:
        return True
    if host.endswith(".youtube.com") or host.endswith(".youtu.be"):
        return True
    return False


def safe_workspace_path(base: Path, *parts: str) -> Path:
    """Resolve `base / parts` and reject if it escapes `base`.

    Prevents path traversal (e.g. `../../etc/passwd`) and symlink escapes.
    """
    base = base.resolve()
    target = (base / Path(*parts)).resolve()
    if target != base and base not in target.parents:
        raise SecurityError(f"path escapes workspace: {target}")
    return target


def run_subprocess(cmd: list[str], timeout: int = 300, **kwargs) -> subprocess.CompletedProcess:
    """Run a subprocess with shell=False and a timeout.

    shell=True is explicitly forbidden.
    """
    if kwargs.pop("shell", False) is True:
        raise SecurityError("shell=True is not allowed")
    return subprocess.run(  # noqa: S603
        cmd, shell=False, timeout=timeout, check=False, **kwargs
    )
