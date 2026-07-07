
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


###########################################################################
# Base Exception
###########################################################################


class AppException(Exception):
    """
    Base application exception.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code


###########################################################################
# Audio Exceptions
###########################################################################


class AudioValidationError(AppException):
    def __init__(self, message: str):
        super().__init__(
            code="AUDIO_VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class UnsupportedAudioTypeError(AppException):
    def __init__(self):
        super().__init__(
            code="UNSUPPORTED_AUDIO_TYPE",
            message="Unsupported audio format.",
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )


class FileTooLargeError(AppException):
    def __init__(self):
        super().__init__(
            code="FILE_TOO_LARGE",
            message="Audio exceeds maximum file size.",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )


###########################################################################
# STT Exceptions
###########################################################################


class STTProviderError(AppException):
    def __init__(self):
        super().__init__(
            code="STT_PROVIDER_ERROR",
            message="Speech-to-text provider failed.",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


###########################################################################
# LLM Exceptions
###########################################################################


class LLMProviderError(AppException):
    def __init__(self):
        super().__init__(
            code="LLM_PROVIDER_ERROR",
            message="Language model provider failed.",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


class InvalidLLMResponse(AppException):
    def __init__(self):
        super().__init__(
            code="INVALID_LLM_RESPONSE",
            message="LLM returned invalid JSON.",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


###########################################################################
# Generic API Exception Handler
###########################################################################


def error_response(
    *,
    request_id: str,
    code: str,
    message: str,
    status_code: int,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
            }
        },
    )


###########################################################################
# Register Exception Handlers
###########################################################################


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):
        request_id = str(uuid4())

        return error_response(
            request_id=request_id,
            code=exc.code,
            message=exc.message,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        request_id = str(uuid4())

        return error_response(
            request_id=request_id,
            code="VALIDATION_ERROR",
            message="Invalid request payload.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        request_id = str(uuid4())

        return error_response(
            request_id=request_id,
            code="HTTP_EXCEPTION",
            message=str(exc.detail),
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        request_id = str(uuid4())

        return error_response(
            request_id=request_id,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )