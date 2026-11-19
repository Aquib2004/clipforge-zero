"""Structured logging with secret redaction.

API keys, tokens, authorization headers and similar secrets are redacted
from log output so they never appear in console or file logs.
"""

import logging
import re
import sys

_SECRET_PATTERNS = [
    re.compile(r"(api[_-]?key|apikey)[\"'\s:]+([^\"'\s,}]+)", re.IGNORECASE),
    re.compile(r"(authorization|bearer)[\"'\s:]+([^\"'\s,}]+)", re.IGNORECASE),
    re.compile(r"(access[_-]?token|token)[\"'\s:]+([^\"'\s,}]+)", re.IGNORECASE),
    re.compile(r"(client[_-]?secret)[\"'\s:]+([^\"'\s,}]+)", re.IGNORECASE),
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
    re.compile(r"gho_[A-Za-z0-9]{36,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
]


def redact(value: str) -> str:
    """Redact secret-like substrings from a log message."""
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub(r"\1=***REDACTED***", value)
    return value


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        return redact(msg)


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(RedactingFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
