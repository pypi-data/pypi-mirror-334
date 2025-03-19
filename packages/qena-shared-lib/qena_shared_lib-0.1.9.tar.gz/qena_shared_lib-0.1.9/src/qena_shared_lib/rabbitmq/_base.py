from abc import ABC
from asyncio import (
    Future,
    Task,
    gather,
    iscoroutinefunction,
)
from dataclasses import dataclass
from functools import partial
from inspect import Parameter, signature
from random import uniform
from typing import (
    Awaitable,
    Callable,
    Concatenate,
    ParamSpec,
    TypeVar,
)

from pika.adapters.asyncio_connection import AsyncioConnection
from pika.connection import Parameters, URLParameters
from pika.exceptions import ChannelClosedByClient, ConnectionClosedByClient
from pika.frame import Method
from prometheus_client import Counter
from prometheus_client import Enum as PrometheusEnum
from punq import Container, Scope
from pydantic import ValidationError

from ..dependencies.miscellaneous import validate_annotation
from ..exceptions import (
    RabbitMQConnectionUnhealthyError,
    ServiceException,
)
from ..logging import LoggerProvider
from ..logstash import BaseLogstashSender
from ..utils import AsyncEventLoopMixin
from ._exception_handlers import (
    handle_general_mq_exception,
    handle_rabbit_mq_service_exception,
    handle_validation_error,
)
from ._listener import (
    LISTENER_ATTRIBUTE,
    Listener,
    ListenerBase,
    ListenerContext,
    RetryPolicy,
)
from ._pool import ChannelPool
from ._publisher import Publisher
from ._rpc_client import RpcClient

__all__ = [
    "AbstractRabbitMQService",
    "RabbitMqManager",
]

E = TypeVar("E")
P = ParamSpec("P")
ExceptionHandler = (
    Callable[Concatenate[ListenerContext, E, P], None]
    | Callable[Concatenate[ListenerContext, E, P], Awaitable]
)


class AbstractRabbitMQService(ABC):
    def initialize(
        self, connection: AsyncioConnection, channel_pool: ChannelPool
    ) -> Future:
        raise NotImplementedError()


@dataclass
class ExceptionHandlerContainer:
    handler: ExceptionHandler
    dependencies: dict[str, type]


class RabbitMqManager(AsyncEventLoopMixin):
    RABBITMQ_CONNECTION_STATE = PrometheusEnum(
        name="rabbitmq_connection_state",
        documentation="Babbitmq connection state",
        states=["connected", "reconnecting", "disconnected"],
    )
    RABBITMQ_PUBLISHER_BLOCKED_STATE = PrometheusEnum(
        name="rabbitmq_publisher_blocked_state",
        documentation="Rabbitmq publisher blocked state",
        states=["blocked", "unblocked"],
    )
    HANDLED_EXCEPTIONS = Counter(
        name="handled_exceptions",
        documentation="Handled exceptions",
        labelnames=["queue", "listener_name", "exception"],
    )

    def __init__(
        self,
        logstash: BaseLogstashSender,
        parameters: Parameters | str | None = None,
        reconnect_delay: float = 5.0,
        reconnect_delay_jitter: tuple[float, float] = (1.0, 5.0),
        listener_global_retry_policy: RetryPolicy | None = None,
        container: Container | None = None,
    ):
        self._listeners: list[Listener] = []

        if isinstance(parameters, str):
            self._parameters = URLParameters(parameters)
        else:
            self._parameters = parameters

        self._reconnect_delay = reconnect_delay
        self._reconnect_delay_jitter = reconnect_delay_jitter
        self._container = container or Container()
        self._listener_global_retry_policy = listener_global_retry_policy
        self._connection = None
        self._connected = False
        self._disconnected = False
        self._connection_blocked = False
        self._services = []
        self._exception_handlers: dict[
            type[Exception], ExceptionHandlerContainer
        ] = {}

        self.exception_handler(ServiceException)(
            handle_rabbit_mq_service_exception
        )
        self.exception_handler(ValidationError)(handle_validation_error)
        self.exception_handler(Exception)(handle_general_mq_exception)

        self._channel_pool = ChannelPool()
        self._logstash = logstash
        self._logger = LoggerProvider.default().get_logger("rabbitmq")

    @property
    def container(self) -> Container:
        return self._container

    def exception_handler(
        self, exception: type[Exception]
    ) -> Callable[[ExceptionHandler], ExceptionHandler]:
        if not issubclass(exception, Exception):
            raise TypeError(
                f"exception should be of type `Exception`, got {exception}"
            )

        def wrapper(
            handler: ExceptionHandler,
        ):
            if not callable(handler):
                raise TypeError(f"handler not a callable, got {type(handler)}")

            dependencies = {}

            for parameter_position, (parameter_name, parameter) in enumerate(
                signature(handler).parameters.items()
            ):
                if 0 <= parameter_position < 2:
                    is_valid, expected_type = (
                        self._is_valid_exception_handler_parameter(
                            position=parameter_position,
                            annotation=parameter.annotation,
                        )
                    )

                    if not is_valid:
                        raise TypeError(
                            f"parameter `{parameter_name}` at `{parameter_position + 1}` is not annotated with type or subclass of `{expected_type}`, got {parameter.annotation}"
                        )

                    continue

                dependency = validate_annotation(parameter)

                if dependency is None:
                    raise ValueError(
                        f"handlers cannot contain parameters other than `Annotated[type, DependsOn(type)]`, got `{parameter_name}: {dependency}`"
                    )

                dependencies[parameter_name] = dependency

            self._exception_handlers[exception] = ExceptionHandlerContainer(
                handler=handler, dependencies=dependencies
            )

            return handler

        return wrapper

    def _is_valid_exception_handler_parameter(
        self, position: int, annotation: type
    ) -> tuple[bool, type | None]:
        if annotation is Parameter.empty:
            return True, None

        if position == 0 and annotation is not ListenerContext:
            return False, ListenerContext

        if position == 1 and not issubclass(annotation, Exception):
            return False, Exception

        return True, None

    def include_listener(self, listener: Listener | type[ListenerBase]):
        if isinstance(listener, Listener):
            self._listeners.append(listener)

            return

        if isinstance(listener, type) and issubclass(listener, ListenerBase):
            self._register_listener_classes(listener)

            return

        raise TypeError(
            f"listener is {type(listener)}, expected instance of type or subclass of `Listener` or `type[ListenerBase]`"
        )

    def _register_listener_classes(self, listener_class: type):
        inner_listener = getattr(listener_class, LISTENER_ATTRIBUTE, None)

        if inner_listener is None:
            raise AttributeError(
                "listener is possibly not with `Consumer` or `RpcWorker`"
            )

        if not isinstance(inner_listener, Listener):
            raise TypeError(
                f"listener class {type(listener_class)} is not a type `Listener`, posibilly not decorated with `Consumer` or `RpcWorker`"
            )

        self._container.register(
            service=ListenerBase,
            factory=listener_class,
            scope=Scope.singleton,
        )

    def include_service(
        self,
        rabbit_mq_service: AbstractRabbitMQService
        | type[AbstractRabbitMQService],
    ):
        if not isinstance(rabbit_mq_service, AbstractRabbitMQService) and (
            not isinstance(rabbit_mq_service, type)
            or not issubclass(rabbit_mq_service, AbstractRabbitMQService)
        ):
            raise TypeError(
                f"rabbitmq service is not type of `AbstractRabbitMQService`, got `{type(rabbit_mq_service)}`"
            )

        if isinstance(rabbit_mq_service, AbstractRabbitMQService):
            self._services.append(rabbit_mq_service)
        else:
            self._container.register(
                service=AbstractRabbitMQService,
                factory=rabbit_mq_service,
                scope=Scope.singleton,
            )

    def connect(self) -> Future:
        if not self._connected:
            self._resolve_listener_classes()
            self._resolve_service_classes()

        if self._is_connection_healthy():
            raise RuntimeError("rabbitmq already connected and healthy")

        self._connected_future = self.loop.create_future()
        _ = AsyncioConnection(
            parameters=self._parameters,
            on_open_callback=self._on_connection_opened,
            on_open_error_callback=self._on_connection_open_error,
            on_close_callback=self._on_connection_closed,
            custom_ioloop=self.loop,
        )

        return self._connected_future

    def _resolve_listener_classes(self):
        self._listeners.extend(
            listener.register_listener_methods()
            for listener in self._container.resolve_all(ListenerBase)
        )

    def _resolve_service_classes(self):
        self._services.extend(
            self._container.resolve_all(AbstractRabbitMQService)
        )

    @property
    def connection(self) -> AsyncioConnection:
        if not self._is_connection_healthy():
            raise RabbitMQConnectionUnhealthyError("connection not ready yet")

        assert self._connection is not None

        return self._connection

    def publisher(
        self,
        routing_key: str,
        exchange: str | None = None,
        target: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> Publisher:
        if not self._is_connection_healthy():
            raise RabbitMQConnectionUnhealthyError(
                "rabbitmq connection is not healthy"
            )

        return Publisher(
            routing_key=routing_key,
            channel_pool=self._channel_pool,
            blocked_connection_check_callback=self._is_connection_blocked,
            exchange=exchange,
            target=target,
            headers=headers,
        )

    def rpc_client(
        self,
        routing_key: str,
        exchange: str | None = None,
        procedure: str | None = None,
        headers: dict[str, str] | None = None,
        return_type: type | None = None,
        timeout: float = 0,
    ) -> RpcClient:
        if timeout == 0:
            self._logger.warning(
                "rpc call with 0 seconds timeout may never return back"
            )

        if not self._is_connection_healthy():
            raise RabbitMQConnectionUnhealthyError(
                "rabbitmq connection is not healthy"
            )

        return RpcClient(
            routing_key=routing_key,
            channel_pool=self._channel_pool,
            blocked_connection_check_callback=self._is_connection_blocked,
            exchange=exchange,
            procedure=procedure,
            headers=headers,
            return_type=return_type,
            timeout=abs(timeout),
        )

    def _is_connection_healthy(self) -> bool:
        return (
            self._connected
            and self._connection is not None
            and not self._connection.is_closing
            and not self._connection.is_closed
        )

    def disconnect(self):
        if self._disconnected:
            raise RuntimeError("already disconnected from rabbitmq")

        self._disconnected = True

        if self._connection is None:
            raise RabbitMQConnectionUnhealthyError("connection not ready yet")

        if self._connection.is_closing or self._connection.is_closed:
            self._logger.info("already disconnected from rabbitmq")
        else:
            self._connection.close()
            self._logger.info("disconnected from rabbitmq")

        self.RABBITMQ_CONNECTION_STATE.state("disconnected")

    def _on_connection_opened(self, connection: AsyncioConnection):
        self._connection = connection
        self._connection_blocked = False

        self._connection.add_on_connection_blocked_callback(
            self._on_connection_blocked
        )
        self._connection.add_on_connection_unblocked_callback(
            self._on_connection_unblocked
        )

        if self._connected:
            self.loop.create_task(self._channel_pool.drain()).add_done_callback(
                self._channel_pool_drained
            )

            return

        self.loop.create_task(
            self._channel_pool.fill(self._connection)
        ).add_done_callback(self._channel_pool_filled)

    def _channel_pool_drained(self, task: Task):
        if task.cancelled():
            if not self._connected and not self._connected_future.done():
                _ = self._connected_future.cancel(None)

            return

        exception = task.exception()

        if exception is not None:
            if self._can_reconnect(exception):
                self._logstash.error(
                    message="couldn't drain the channel pool",
                    exception=exception,
                )
                self._reconnect()

            return

        if self._connection is None:
            raise RabbitMQConnectionUnhealthyError("connection not ready yet")

        self.loop.create_task(
            self._channel_pool.fill(self._connection)
        ).add_done_callback(self._channel_pool_filled)

    def _on_connection_blocked(
        self, connection: AsyncioConnection, method: Method
    ):
        del connection, method

        self._connection_blocked = True

        self._logstash.warning(
            "connection is blocked by broker, will not accept published messages"
        )
        self.RABBITMQ_PUBLISHER_BLOCKED_STATE.state("blocked")

    def _on_connection_unblocked(
        self, connection: AsyncioConnection, method: Method
    ):
        del connection, method

        self._connection_blocked = False

        self._logstash.info("broker resumed accepting published messages")
        self.RABBITMQ_PUBLISHER_BLOCKED_STATE.state("unblocked")

    def _is_connection_blocked(self) -> bool:
        return self._connection_blocked

    def _channel_pool_filled(self, task: Task):
        if task.cancelled():
            if not self._connected and not self._connected_future.done():
                _ = self._connected_future.cancel(None)

            return

        exception = task.exception()

        if exception is not None:
            if not self._connected and not self._connected_future.done():
                self._connected_future.set_exception(exception)
            elif self._can_reconnect(exception):
                self._logstash.error(
                    message="couldn't fill the channel pool",
                    exception=exception,
                )
                self._reconnect()

            return

        if self._connection is None:
            raise RabbitMQConnectionUnhealthyError("connection not ready yet")

        channel_count = len(self._channel_pool)

        self._logger.debug(
            "global channel pool filled with `%d` %s",
            channel_count,
            "channel" if 0 <= channel_count <= 1 else "channels",
        )
        gather(
            *self._configure_listeners(), *self._initialize_services()
        ).add_done_callback(self._listener_and_service_config_and_init_done)

    def _configure_listeners(self) -> list[Awaitable]:
        try:
            assert self._connection is not None

            return [
                listener.configure(
                    connection=self._connection,
                    channel_pool=self._channel_pool,
                    on_exception_callback=self._invoke_exception_handler,
                    container=self._container,
                    logstash=self._logstash,
                    global_retry_policy=self._listener_global_retry_policy,
                )
                for listener in self._listeners
            ]
        except Exception as e:
            listener_configuration_error_future = self.loop.create_future()

            listener_configuration_error_future.set_exception(e)

            return [listener_configuration_error_future]

    def _initialize_services(self) -> list[Awaitable]:
        try:
            return [
                service.initialize(self._connection, self._channel_pool)
                for service in self._services
            ]
        except Exception as e:
            service_initialization_error_future = self.loop.create_future()

            service_initialization_error_future.set_exception(e)

            return [service_initialization_error_future]

    def _listener_and_service_config_and_init_done(self, future: Future):
        if future.cancelled():
            if not self._connected and not self._connected_future.done():
                _ = self._connected_future.cancel(None)

            return

        exception = future.exception()

        if exception is not None:
            if not self._connected and not self._connected_future.done():
                self._connected_future.set_exception(exception)
            elif self._can_reconnect(exception):
                self._logstash.error(
                    message="couldn't configure and initialize all listeners and services",
                    exception=exception,
                )
                self._reconnect()

            return

        if not self._connected:
            self._connected = True

        if self._connection is None:
            raise RabbitMQConnectionUnhealthyError("connection not ready yet")

        params = self._connection.params
        listener_count = len(self._listeners)
        service_count = len(self._services)

        self._logger.info(
            "connect to rabbitmq, `%s:%s%s` with `%d` %s and `%d` %s.",
            params.host,
            params.port,
            params.virtual_host,
            listener_count,
            "listeners" if listener_count > 1 else "listener",
            service_count,
            "services" if service_count > 1 else "service",
        )

        if not self._connected_future.done():
            self._connected_future.set_result(None)

        self.RABBITMQ_CONNECTION_STATE.state("connected")

    def _on_connection_open_error(
        self, connection: AsyncioConnection, exception: BaseException
    ):
        del connection

        if not self._connected and not self._connected_future.done():
            self._connected_future.set_exception(exception)

            return

        if self._connected and not self._disconnected:
            self._logstash.error(
                message="error while opening connection to rabbitmq",
                exception=exception,
            )
            self._reconnect()

    def _invoke_exception_handler(
        self, context: ListenerContext, exception: BaseException
    ) -> bool:
        exception_handler = None

        for exception_type in type(exception).mro():
            exception_handler = self._exception_handlers.get(exception_type)

            if exception_handler is not None:
                break

        if exception_handler is None:
            return False

        dependencies = {}

        for (
            parameter_name,
            dependency,
        ) in exception_handler.dependencies.items():
            dependencies[parameter_name] = self._container.resolve(dependency)

        if iscoroutinefunction(exception_handler.handler):
            self.loop.create_task(
                exception_handler.handler(context, exception, **dependencies)
            ).add_done_callback(
                partial(self._on_exception_handler_done, context)
            )
        else:
            self.loop.run_in_executor(
                executor=None,
                func=partial(
                    exception_handler.handler,
                    context,
                    exception,
                    **dependencies,
                ),
            ).add_done_callback(
                partial(self._on_exception_handler_done, context)
            )

        self.HANDLED_EXCEPTIONS.labels(
            queue=context.queue,
            listener_name=context.listener_name,
            exception=exception.__class__.__name__,
        ).inc()

        return True

    def _on_exception_handler_done(
        self, context: ListenerContext, task_or_future: Task | Future
    ):
        if task_or_future.cancelled():
            return

        exception = task_or_future.exception()

        if exception is not None:
            self._logstash.error(
                message="error occured in listener exception handler",
                exception=exception,
            )

        context.dispose()

    def _on_connection_closed(
        self, connection: AsyncioConnection, exception: BaseException
    ):
        del connection

        if not self._connected and not self._connected_future.done():
            self._connected_future.set_exception(exception)

            return

        if self._can_reconnect(exception):
            self._logstash.error(
                message="connection to rabbitmq closed unexpectedly, attempting to reconnect",
                exception=exception,
            )
            self._reconnect()

    def _reconnect(self):
        self.RABBITMQ_CONNECTION_STATE.state("reconnecting")
        self.loop.call_later(
            delay=self._reconnect_delay
            + uniform(*self._reconnect_delay_jitter),
            callback=self._on_time_to_reconnect,
        )

    def _on_time_to_reconnect(self):
        try:
            connected_future = self.connect()
        except Exception as e:
            if self._can_reconnect(e):
                if not self._connected_future.done():
                    self._connected_future.set_result(None)

                self._logstash.exception(
                    "couldn't reconnect to rabbitmq, attempting to reconnect"
                )
                self._reconnect()

            return

        if connected_future.done():
            return

        connected_future.add_done_callback(self._on_reconnect_done)

    def _on_reconnect_done(self, future: Future):
        if future.cancelled():
            return

        exception = future.exception()

        if exception is None:
            return

        if self._can_reconnect(exception):
            self._logstash.error(
                message="couldn't reconnect to rabbitmq, attempting to reconnect",
                exception=exception,
            )
            self._reconnect()

    def _can_reconnect(self, exception: BaseException) -> bool:
        return (
            self._connected
            and not self._disconnected
            and not isinstance(
                exception, (ConnectionClosedByClient, ChannelClosedByClient)
            )
        )
