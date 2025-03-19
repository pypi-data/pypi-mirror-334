from typing import Annotated

from pydantic import ValidationError

from ..dependencies.miscellaneous import DependsOn
from ..exceptions import (
    HTTPServiceError,
    RabbitMQServiceException,
    ServiceException,
    Severity,
)
from ..logging import LoggerProvider
from ..logstash._base import BaseLogstashSender
from ._listener import ListenerContext

__all__ = [
    "handle_general_mq_exception",
    "handle_rabbit_mq_service_exception",
    "handle_validation_error",
]

RABBITMQ_EXCEPTION_HANDLER_LOGGER_NAME = "rabbitmq.exception_handler"


def handle_rabbit_mq_service_exception(
    context: ListenerContext,
    exception: ServiceException,
    logstash: Annotated[BaseLogstashSender, DependsOn(BaseLogstashSender)],
    logger_provider: Annotated[LoggerProvider, DependsOn(LoggerProvider)],
):
    logger = logger_provider.get_logger(RABBITMQ_EXCEPTION_HANDLER_LOGGER_NAME)
    tags = [
        "RabbitMQ",
        context.queue,
        context.listener_name or "__default__",
        exception.__class__.__name__,
    ]
    extra = {
        "serviceType": "RabbitMQ",
        "queue": context.queue,
        "listenerName": context.listener_name,
        "exception": exception.__class__.__name__,
    }

    match exception:
        case HTTPServiceError() as http_service_error:
            if http_service_error.status_code is not None:
                str_status_code = str(http_service_error.status_code)
                extra["statusCode"] = str_status_code

                tags.append(str_status_code)

            if http_service_error.response_code is not None:
                str_response_code = str(http_service_error.response_code)
                extra["responseCode"] = str_response_code

                tags.append(str_response_code)
        case RabbitMQServiceException() as rabbitmq_service_exception:
            str_error_code = str(rabbitmq_service_exception.code)
            extra["code"] = str_error_code

            tags.append(str_error_code)

    if exception.tags:
        tags.extend(exception.tags)

    if exception.extra:
        extra.update(exception.extra)

    exc_info = (
        (type(exception), exception, exception.__traceback__)
        if exception.extract_exc_info
        else None
    )

    match exception.severity:
        case Severity.HIGH:
            logstash_logger_method = logstash.error
            logger_method = logger.error
        case Severity.MEDIUM:
            logstash_logger_method = logstash.warning
            logger_method = logger.warning
        case _:
            logstash_logger_method = logstash.info
            logger_method = logger.info

    if exception.logstash_logging:
        logstash_logger_method(
            message=exception.message,
            tags=tags,
            extra=extra,
            exception=exception if exception.extract_exc_info else None,
        )
    else:
        logger_method(
            "\nRabbitMQ `%s` -> `%s`\n%s",
            context.queue,
            context.listener_name,
            exception.message,
            exc_info=exc_info,
        )


def handle_validation_error(
    context: ListenerContext,
    exception: ValidationError,
    logstash: Annotated[BaseLogstashSender, DependsOn(BaseLogstashSender)],
):
    logstash.error(
        message=f"invalid rabbitmq request data at queue `{context.queue}` and listener `{context.listener_name}`",
        tags=[
            "RabbitMQ",
            context.queue,
            context.listener_name or "__default__",
            "ValidationError",
        ],
        extra={
            "serviceType": "RabbitMQ",
            "queue": context.queue,
            "listenerName": context.listener_name,
            "exception": "ValidationError",
        },
        exception=exception,
    )


def handle_general_mq_exception(
    context: ListenerContext,
    exception: Exception,
    logstash: Annotated[BaseLogstashSender, DependsOn(BaseLogstashSender)],
):
    logstash.error(
        message=f"something went wrong while consuming message on queue `{context.queue}` and listener `{context.listener_name}`",
        tags=[
            "RabbitMQ",
            context.queue,
            context.listener_name or "__default__",
            exception.__class__.__name__,
        ],
        extra={
            "serviceType": "RabbitMQ",
            "queue": context.queue,
            "listenerName": context.listener_name,
            "exception": exception.__class__.__name__,
        },
        exception=exception,
    )
