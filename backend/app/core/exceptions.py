"""Application exception hierarchy with consistent error codes and status codes."""


class ClipForgeError(Exception):
    def __init__(self, message: str, code: str = "error", status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundError(ClipForgeError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, code="not_found", status_code=404)


class ValidationError(ClipForgeError):
    def __init__(self, message: str):
        super().__init__(message, code="validation_error", status_code=400)


class SecurityError(ClipForgeError):
    def __init__(self, message: str):
        super().__init__(message, code="security_error", status_code=403)
