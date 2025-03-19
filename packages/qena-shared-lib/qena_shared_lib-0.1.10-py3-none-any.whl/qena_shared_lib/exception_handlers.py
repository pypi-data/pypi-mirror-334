from collections.abc import Iterable
from typing import Any

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import to_jsonable_python

from .dependencies.http import get_service
from .exceptions import (
    HTTPServiceError,
    RabbitMQServiceException,
    ServiceException,
    Severity,
)
from .logging import LoggerProvider
from .logstash._base import BaseLogstashSender

__all__ = [
    "handle_http_service_error",
    "handle_request_validation_error",
    "handle_general_http_exception",
]


def handle_http_service_error(
    request: Request, exception: ServiceException
) -> Response:
    logstash = get_service(app=request.app, service_key=BaseLogstashSender)
    logger_provider = get_service(app=request.app, service_key=LoggerProvider)
    logger = logger_provider.get_logger("http.exception_handler")
    exception_severity = exception.severity or Severity.LOW
    message = exception.message
    tags = [
        "HTTP",
        request.method,
        request.url.path,
        exception.__class__.__name__,
    ]
    extra = {
        "serviceType": "HTTP",
        "method": request.method,
        "path": request.url.path,
        "exception": exception.__class__.__name__,
    }
    exc_info = (
        (type(exception), exception, exception.__traceback__)
        if exception.extract_exc_info
        else None
    )

    match exception_severity:
        case Severity.LOW:
            logstash_logger_method = logstash.info
            logger_method = logger.info
        case Severity.MEDIUM:
            logstash_logger_method = logstash.warning
            logger_method = logger.warning
        case _:
            message = "something went wrong"
            logstash_logger_method = logstash.error
            logger_method = logger.error

    content: dict[str, Any] = {
        "severity": exception_severity.name,
        "message": message,
    }
    status_code = _status_code_from_severity(exception.severity)
    headers = None

    match exception:
        case HTTPServiceError() as http_service_error:
            if http_service_error.body is not None:
                extra_body = to_jsonable_python(http_service_error.body)
                is_updated = False

                try:
                    if isinstance(extra_body, Iterable):
                        content.update(extra_body)

                        is_updated = True
                except:
                    pass

                if not is_updated:
                    content["data"] = extra_body

            if http_service_error.response_code is not None:
                content["code"] = http_service_error.response_code
                str_response_code = str(http_service_error.response_code)
                extra["responseCode"] = str_response_code

                tags.append(str_response_code)

            if http_service_error.corrective_action is not None:
                content["correctiveAction"] = (
                    http_service_error.corrective_action
                )

            if http_service_error.status_code is not None:
                status_code = http_service_error.status_code
                str_status_code = str(status_code)
                extra["statusCode"] = str_status_code

                tags.append(str_status_code)

            if http_service_error.headers is not None:
                headers = http_service_error.headers
        case RabbitMQServiceException() as rabbitmq_service_exception:
            str_error_code = str(rabbitmq_service_exception.code)
            extra["code"] = str_error_code

            tags.append(str_error_code)

    if exception.tags:
        tags.extend(exception.tags)

    if exception.extra:
        extra.update(exception.extra)

    if exception.logstash_logging:
        logstash_logger_method(
            message=exception.message,
            tags=tags,
            extra=extra,
            exception=exception if exception.extract_exc_info else None,
        )
    else:
        logger_method(
            "\n%s %s\n%s",
            request.method,
            request.url.path,
            exception.message,
            exc_info=exc_info,
        )

    return JSONResponse(
        content=content,
        status_code=status_code,
        headers=headers,
    )


def handle_request_validation_error(
    request: Request, error: RequestValidationError
) -> Response:
    logger_provider = get_service(app=request.app, service_key=LoggerProvider)
    logger = logger_provider.get_logger("http.exception_handler")
    message = "invalid request data"

    logger.warning("\n%s %s\n%s", request.method, request.url.path, message)

    return JSONResponse(
        content={
            "severity": Severity.MEDIUM.name,
            "message": message,
            "code": 100,
            "detail": to_jsonable_python(error.errors()),
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def handle_general_http_exception(
    request: Request, exception: Exception
) -> Response:
    logstash = get_service(app=request.app, service_key=BaseLogstashSender)

    logstash.error(
        message=f"something went wrong on endpoint `{request.method} {request.url.path}`",
        tags=[
            "HTTP",
            request.method,
            request.url.path,
            exception.__class__.__name__,
        ],
        extra={
            "serviceType": "HTTP",
            "method": request.method,
            "path": request.url.path,
            "exception": exception.__class__.__name__,
        },
        exception=exception,
    )

    return JSONResponse(
        content={
            "severity": Severity.HIGH.name,
            "message": "something went wrong",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _status_code_from_severity(severity: Severity | None) -> int:
    if (
        severity is None
        or severity == Severity.LOW
        or severity == Severity.MEDIUM
    ):
        return status.HTTP_400_BAD_REQUEST

    return status.HTTP_500_INTERNAL_SERVER_ERROR
