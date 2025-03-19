from enum import Enum
from typing import Any

__all__ = [
    "BadGateway",
    "BadRequest",
    "ClientError",
    "Conflict",
    "ExpectationFailed",
    "FailedDependency",
    "Forbidden",
    "GatewayTimeout",
    "Gone",
    "HTTPServiceError",
    "HTTPVersionNotSupported",
    "IAmATeapot",
    "InsufficientStorage",
    "InternalServerError",
    "LengthRequired",
    "Locked",
    "LoopDetected",
    "MethodNotAllowed",
    "MisdirectedRequest",
    "NetworkAuthenticationRequired",
    "NotAcceptable",
    "NotExtended",
    "NotFound",
    "NotImplemented",
    "PayloadTooLarge",
    "PaymentRequired",
    "PreconditionFailed",
    "PreconditionRequired",
    "ProxyAuthenticationRequired",
    "RabbitMQBlockedError",
    "RabbitMQConnectionUnhealthyError",
    "RabbitMQRpcRequestPendingError",
    "RabbitMQRpcRequestTimeoutError",
    "RabbitMQServiceException",
    "RangeNotSatisfiable",
    "RequestHeaderFieldsTooLarge",
    "RequestTimeout",
    "ServerError",
    "ServiceException",
    "ServiceUnavailable",
    "Severity",
    "TooEarly",
    "TooManyRequests",
    "Unauthorized",
    "UnavailableForLegalReasons",
    "UnprocessableEntity",
    "UnsupportedMediaType",
    "UpgradeRequired",
    "URITooLong",
    "VariantAlsoNegotiates",
]


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class ServiceException(Exception):
    _GENERAL_SEVERITY = None
    _GENERAL_EXTRACT_EXC_INFO = None

    def __init__(
        self,
        message: str,
        severity: Severity | None = None,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        logstash_logging: bool | None = None,
        extract_exc_info: bool | None = None,
    ):
        self._message = message

        if severity is not None:
            self._severity = severity
        else:
            self._severity = self._GENERAL_SEVERITY

        self._tags = tags
        self._extra = extra

        if logstash_logging is not None:
            self._logstash_logging = logstash_logging
        else:
            self._logstash_logging = True

        if extract_exc_info is not None:
            self._extract_exc_info = extract_exc_info
        else:
            self._extract_exc_info = self._GENERAL_EXTRACT_EXC_INFO

    @property
    def message(self) -> str:
        return self._message

    @property
    def severity(self) -> Severity | None:
        return self._severity

    @property
    def tags(self) -> list[str] | None:
        return self._tags

    @property
    def extra(self) -> dict[str, str] | None:
        return self._extra

    @property
    def logstash_logging(self) -> bool | None:
        return self._logstash_logging

    @property
    def extract_exc_info(self) -> bool | None:
        return self._extract_exc_info

    def __str__(self) -> str:
        return f"message `{self._message}`, tags {self._tags or []}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ( message: `{self._message}`, tags: {self._tags or []}, extra: {self._extra or {}} )"


class HTTPServiceError(ServiceException):
    _GENERAL_STATUS_CODE = None

    def __init__(
        self,
        message: str,
        body: Any | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
        response_code: int | None = None,
        corrective_action: str | None = None,
        severity: Severity | None = None,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        logstash_logging: bool = True,
        extract_exc_info: bool = True,
    ):
        super().__init__(
            message=message,
            severity=severity,
            tags=tags,
            extra=extra,
            logstash_logging=logstash_logging,
            extract_exc_info=extract_exc_info,
        )

        self._body = body

        if status_code is not None:
            self._status_code = status_code
        else:
            self._status_code = self._GENERAL_STATUS_CODE

        self._headers = headers
        self._response_code = response_code
        self._corrective_action = corrective_action

    @property
    def body(self) -> Any | None:
        return self._body

    @property
    def status_code(self) -> int | None:
        return self._status_code

    @property
    def headers(self) -> dict[str, str] | None:
        return self._headers

    @property
    def response_code(self) -> int | None:
        return self._response_code

    @property
    def corrective_action(self) -> str | None:
        return self._corrective_action

    def __str__(self) -> str:
        return f"message `{self._message}`, status_code {self._status_code or 500}, response_code {self._response_code or 0}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ( message: `{self._message}`, status_code: {self._status_code or 500}, response_code: {self._response_code or 0} )"


class ClientError(HTTPServiceError):
    _GENERAL_EXTRACT_EXC_INFO = False
    _GENERAL_SEVERITY = Severity.MEDIUM


class BadRequest(ClientError):
    _GENERAL_STATUS_CODE = 400


class Unauthorized(ClientError):
    _GENERAL_STATUS_CODE = 401


class PaymentRequired(ClientError):
    _GENERAL_STATUS_CODE = 402


class Forbidden(ClientError):
    _GENERAL_STATUS_CODE = 403


class NotFound(ClientError):
    _GENERAL_STATUS_CODE = 404


class MethodNotAllowed(ClientError):
    _GENERAL_STATUS_CODE = 405


class NotAcceptable(ClientError):
    _GENERAL_STATUS_CODE = 406


class ProxyAuthenticationRequired(ClientError):
    _GENERAL_STATUS_CODE = 407


class RequestTimeout(ClientError):
    _GENERAL_STATUS_CODE = 408


class Conflict(ClientError):
    _GENERAL_STATUS_CODE = 409


class Gone(ClientError):
    _GENERAL_STATUS_CODE = 410


class LengthRequired(ClientError):
    _GENERAL_STATUS_CODE = 411


class PreconditionFailed(ClientError):
    _GENERAL_STATUS_CODE = 412


class PayloadTooLarge(ClientError):
    _GENERAL_STATUS_CODE = 413


class URITooLong(ClientError):
    _GENERAL_STATUS_CODE = 414


class UnsupportedMediaType(ClientError):
    _GENERAL_STATUS_CODE = 415


class RangeNotSatisfiable(ClientError):
    _GENERAL_STATUS_CODE = 416


class ExpectationFailed(ClientError):
    _GENERAL_STATUS_CODE = 417


class IAmATeapot(ClientError):
    _GENERAL_STATUS_CODE = 418


class MisdirectedRequest(ClientError):
    _GENERAL_STATUS_CODE = 421


class UnprocessableEntity(ClientError):
    _GENERAL_STATUS_CODE = 422


class Locked(ClientError):
    _GENERAL_STATUS_CODE = 423


class FailedDependency(ClientError):
    _GENERAL_STATUS_CODE = 424


class TooEarly(ClientError):
    _GENERAL_STATUS_CODE = 425


class UpgradeRequired(ClientError):
    _GENERAL_STATUS_CODE = 426


class PreconditionRequired(ClientError):
    _GENERAL_STATUS_CODE = 428


class TooManyRequests(ClientError):
    _GENERAL_STATUS_CODE = 429


class RequestHeaderFieldsTooLarge(ClientError):
    _GENERAL_STATUS_CODE = 431


class UnavailableForLegalReasons(ClientError):
    _GENERAL_STATUS_CODE = 451


class ServerError(HTTPServiceError):
    _GENERAL_EXTRACT_EXC_INFO = True
    _GENERAL_SEVERITY = Severity.HIGH


class InternalServerError(ServerError):
    _GENERAL_STATUS_CODE = 500


class NotImplemented(ServerError):
    _GENERAL_STATUS_CODE = 501


class BadGateway(ServerError):
    _GENERAL_STATUS_CODE = 502


class ServiceUnavailable(ServerError):
    _GENERAL_STATUS_CODE = 503


class GatewayTimeout(ServerError):
    _GENERAL_STATUS_CODE = 504


class HTTPVersionNotSupported(ServerError):
    _GENERAL_STATUS_CODE = 505


class VariantAlsoNegotiates(ServerError):
    _GENERAL_STATUS_CODE = 506


class InsufficientStorage(ServerError):
    _GENERAL_STATUS_CODE = 507


class LoopDetected(ServerError):
    _GENERAL_STATUS_CODE = 508


class NotExtended(ServerError):
    _GENERAL_STATUS_CODE = 510


class NetworkAuthenticationRequired(ServerError):
    _GENERAL_STATUS_CODE = 511


class RabbitMQServiceException(ServiceException):
    _GENERAL_SEVERITY = Severity.HIGH
    _GENERAL_CODE = None

    def __init__(
        self,
        message: str,
        code: int | None = None,
        data: Any | None = None,
        severity: Severity | None = None,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        logstash_logging: bool | None = None,
        extract_exc_info: bool | None = None,
    ):
        super().__init__(
            message=message,
            severity=severity,
            tags=tags,
            extra=extra,
            logstash_logging=logstash_logging,
            extract_exc_info=extract_exc_info,
        )

        if code is not None:
            self._code = code
        else:
            self._code = self._GENERAL_CODE or 0

        self._data = data

    @property
    def code(self) -> int:
        return self._code

    @property
    def data(self) -> Any | None:
        return self._data

    def __str__(self) -> str:
        return f"message `{self.message}`, code {self.code}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} ( message: `{self._message}`, code: {self._code} )"


class RabbitMQBlockedError(Exception):
    pass


class RabbitMQRpcRequestTimeoutError(Exception):
    pass


class RabbitMQRpcRequestPendingError(Exception):
    pass


class RabbitMQConnectionUnhealthyError(Exception):
    pass
