from asyncio import (
    Future,
    Queue,
    QueueFull,
    Task,
    gather,
)
from dataclasses import dataclass
from enum import Enum
from sys import exc_info
from traceback import format_exception

from prometheus_client import Counter
from prometheus_client import Enum as PrometheusEnum

from ..logging import LoggerProvider
from ..utils import AsyncEventLoopMixin

__all__ = [
    "BaseLogstashSender",
    "LogLevel",
    "LogstashLogRecord",
]


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class LogstashLogRecord:
    def __init__(
        self,
        message: str,
        service_name: str,
        log_level: LogLevel,
        log_logger: str,
    ):
        self._message = message
        self._service_name = service_name
        self._log_level = log_level
        self._log_logger = log_logger
        self._tags = None
        self._labels = None
        self._error_type = None
        self._error_message = None
        self._error_stack_trace = None
        self._log_retries = 0

    @property
    def message(self) -> str:
        return self._message

    @property
    def service_name(self) -> str:
        return self._service_name

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @property
    def log_logger(self) -> str:
        return self._log_logger

    @property
    def tags(self) -> list[str] | None:
        return self._tags

    @tags.setter
    def tags(self, tags: list[str]):
        self._tags = tags

    @property
    def labels(self) -> dict[str, str] | None:
        return self._labels

    @labels.setter
    def labels(self, labels: dict[str, str]):
        self._labels = labels

    @property
    def error(self) -> tuple[str | None, str | None, str | None]:
        return self._error_type, self._error_message, self._error_stack_trace

    @error.setter
    def error(self, exception: BaseException):
        self._error_type = type(exception).__name__
        self._error_message = str(exception)

        if exception.__traceback__ is not None:
            self._error_stack_trace = "".join(format_exception(exception))

        if self._labels is None:
            self._labels = {}

        self._labels.update(self._extract_exception_cause(exception))

    def _extract_exception_cause(
        self, exception: BaseException
    ) -> dict[str, str]:
        causes = {}
        cause = exception.__cause__ or exception.__context__
        cause_depth = 0

        while cause is not None:
            cause_depth += 1
            causes[self._depth_to_cause(cause_depth)] = cause.__class__.__name__
            cause = cause.__cause__ or cause.__context__

        return causes

    def _depth_to_cause(self, depth: int) -> str:
        match depth:
            case 1:
                return "causeOne"
            case 2:
                return "causeTwo"
            case 3:
                return "causeThree"
            case 4:
                return "causeFour"
            case 5:
                return "causeFive"
            case 6:
                return "causeSix"
            case 7:
                return "causeSeven"
            case 8:
                return "causeEight"
            case 9:
                return "causeNine"
            case _:
                return "causeN"

    def __str__(self) -> str:
        return f"level `{self._log_level.name}`, message `{self._message}`"

    def __repr__(self) -> str:
        return (
            "LogstashLogRecord (\n\tlevel : `%s`,\n\tmessage : `%s`,\n\ttags : %s,\n\tlabel : %s,\n\terror_type : `%s`,\n\terror_message: `%s`\n)%s"
            % (
                self._log_level.name,
                self._message,
                self._tags or [],
                self._labels or {},
                self._error_type or "None",
                self._error_message or "None",
                f"\n{self._error_stack_trace}"
                if self._error_stack_trace is not None
                else "",
            )
        )

    @property
    def log_retries(self) -> int:
        return self._log_retries

    @log_retries.setter
    def log_retries(self, log_retries: int):
        self._log_retries = log_retries

    def to_dict(self) -> dict:
        log: dict[str, str | list | dict[str, str]] = {
            "message": self._message,
            "service.name": self._service_name,
            "log.level": self._log_level.name.lower(),
            "log.logger": self._log_logger,
        }

        if self._tags is not None:
            log["tags"] = self._tags

        if self._labels is not None:
            log["labels"] = self._labels

        if self._error_type is not None:
            log["error.type"] = self._error_type

        if self._error_message is not None:
            log["error.message"] = self._error_message

        if self._error_stack_trace is not None:
            log["error.stack_trace"] = self._error_stack_trace

        return log


@dataclass
class SenderResponse:
    sent: bool
    reason: str | None = None
    should_retry: bool | None = None


class EndOfLogMarker:
    pass


class BaseLogstashSender(AsyncEventLoopMixin):
    LOGSTASH_LOGS = Counter(
        name="successful_logstash_logs",
        documentation="Successfully sent logstash log count",
        labelnames=["log_level"],
    )
    FAILED_LOGSTASH_LOGS = Counter(
        name="failed_logstash_logs",
        documentation="Failed logstash log count",
        labelnames=["log_level", "exception"],
    )
    LOGSTASH_SENDER_STATE = PrometheusEnum(
        name="logstash_sender_state",
        documentation="Logstash sender state",
        states=["running", "stopped"],
    )

    def __init__(
        self,
        service_name: str,
        max_log_retry: int = 5,
        log_queue_size: int = 1000,
        failed_log_queue_size: int = 1000,
    ):
        self._sender = f"qena_shared_lib.logstash.{self.__class__.__name__}"
        self._service_name = service_name
        self._max_log_retry = max_log_retry
        self._started = False
        self._closed = False
        self._log_queue: Queue[LogstashLogRecord | EndOfLogMarker] = Queue(
            log_queue_size
        )
        self._dead_letter_log_queue: Queue[
            LogstashLogRecord | EndOfLogMarker
        ] = Queue(failed_log_queue_size)
        self._level = LogLevel.INFO
        self._logger = LoggerProvider.default().get_logger(
            f"logstash.{self.__class__.__name__.lower()}"
        )

    async def start(self):
        if self._started:
            raise RuntimeError("logstash sender already started")

        self._started = True
        self._closed = False
        self._close_future = self.loop.create_future()
        _, _ = await gather(
            self.loop.run_in_executor(executor=None, func=self._hook_on_start),
            self._hook_on_start_async(),
        )

        self.loop.create_task(self._flush_logs()).add_done_callback(
            self._on_log_flusher_closed
        )
        self._logger.info(
            "logstash logger `%s` started accepting logs",
            self.__class__.__name__,
        )
        self.LOGSTASH_SENDER_STATE.state("running")

    def _hook_on_start(self):
        pass

    async def _hook_on_start_async(self):
        pass

    def _on_log_flusher_closed(self, task: Task):
        if task.cancelled():
            self._close_future.set_result(None)

            return

        exception = task.exception()

        if exception is not None:
            self._close_future.set_exception(exception)

            return

        gather(
            self.loop.run_in_executor(executor=None, func=self._hook_on_stop),
            self._hook_on_stop_async(),
        ).add_done_callback(self._on_close_hook_done)

    def _on_close_hook_done(self, task_or_future: Task | Future):
        if task_or_future.cancelled():
            self._close_future.set_result(None)

            return

        exception = task_or_future.exception()

        if exception is not None:
            self._close_future.set_exception(exception)

            return

        self._close_future.set_result(None)
        self._logger.debug(
            "logstash http logger closed, will no longer accept logs"
        )

    def stop(self) -> Future:
        if self._closed:
            raise RuntimeError("logstash sender already closed")

        self._closed = True
        self._started = False

        try:
            self._log_queue.put_nowait(EndOfLogMarker())
            self._dead_letter_log_queue.put_nowait(EndOfLogMarker())
        except QueueFull:
            pass

        self._close_future.add_done_callback(self._on_close_future_done)

        return self._close_future

    def _on_close_future_done(self, _):
        self.LOGSTASH_SENDER_STATE.state("stopped")

    def _hook_on_stop(self):
        pass

    async def _hook_on_stop_async(self):
        pass

    async def _flush_logs(self):
        while (
            not self._closed
            or not self._log_queue.empty()
            or not self._dead_letter_log_queue.empty()
        ):
            log = None

            if not self._dead_letter_log_queue.empty():
                log = await self._dead_letter_log_queue.get()

                if isinstance(log, LogstashLogRecord):
                    if log.log_retries >= self._max_log_retry:
                        self._logger.exception(
                            "failed to send log too many times, falling back to stdout or stderr. \n%r",
                            log,
                        )

                        continue

                    log.log_retries += 1

            if log is None:
                log = await self._log_queue.get()

            if isinstance(log, EndOfLogMarker):
                if (
                    not self._log_queue.empty()
                    or not self._dead_letter_log_queue.empty()
                ):
                    continue

                break

            try:
                sender_response = await self._send(log)
            except Exception as e:
                self._put_to_dead_letter_log_queue(log)
                self._logger.exception(
                    "error occurred while sending log to logstash"
                )
                self.FAILED_LOGSTASH_LOGS.labels(
                    log_level=log.log_level.name, exception=e.__class__.__name__
                ).inc()

                continue

            if not sender_response.sent:
                if (
                    sender_response.should_retry is None
                    or sender_response.should_retry
                ):
                    self._put_to_dead_letter_log_queue(log)
                else:
                    self._logger.error(
                        "failed log wasn't requeued, falling back to stdout or stderr.\n%r",
                        log,
                    )

                self._logger.warning(
                    "log wasn't sent successfully, reason : %s",
                    sender_response.reason or "No reason",
                )
            else:
                self.LOGSTASH_LOGS.labels(log_level=log.log_level.name).inc()
                self._logger.debug("log sent to logstash.\n%r", log)

    async def _send(self, log: LogstashLogRecord) -> SenderResponse:
        del log

        raise NotImplementedError()

    def _put_to_dead_letter_log_queue(self, log: LogstashLogRecord):
        if self._closed:
            self._logger.error(
                "%s logger closed, falling back to stdout or stderr.\n%r",
                self._sender,
                log,
            )

            return

        try:
            self._dead_letter_log_queue.put_nowait(log)
        except QueueFull:
            self._logger.error(
                "unable to queue log, falling back to stdout or stderr.\n%r",
                log,
            )

    def log(
        self,
        level: LogLevel,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self._enqueue_log(
            level=level,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def debug(
        self,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self._enqueue_log(
            level=LogLevel.DEBUG,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def info(
        self,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self._enqueue_log(
            level=LogLevel.INFO,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def warning(
        self,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self._enqueue_log(
            level=LogLevel.WARNING,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def error(
        self,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        self._enqueue_log(
            level=LogLevel.ERROR,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def exception(
        self,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        if exception is None:
            _, exception, _ = exc_info()

        self.error(
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

    def set_level(self, level: LogLevel):
        self._level = level

    def _enqueue_log(
        self,
        level: LogLevel,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ):
        if self._closed:
            self._logger.warning("Logstash http logger is already close")

            return

        if level.value < self._level.value:
            return

        log = self._construct_log(
            level=level,
            message=message,
            tags=tags,
            extra=extra,
            exception=exception,
        )

        try:
            self._log_queue.put_nowait(log)
        except QueueFull:
            self._put_to_dead_letter_log_queue(log)

    def _construct_log(
        self,
        level: LogLevel,
        message: str,
        tags: list[str] | None = None,
        extra: dict[str, str] | None = None,
        exception: BaseException | None = None,
    ) -> LogstashLogRecord:
        log = LogstashLogRecord(
            message=message,
            service_name=self._service_name,
            log_level=level,
            log_logger=self._sender,
        )

        if tags is not None:
            log.tags = tags

        if extra is not None and all(
            isinstance(k, str) and isinstance(v, str)
            for (k, v) in extra.items()
        ):
            log.labels = extra

        if exception:
            log.error = exception

        return log
