from enum import Enum
from typing import TypeVar

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
from punq import Container, Scope, empty
from starlette.types import Lifespan

from .exception_handlers import (
    handle_general_http_exception,
    handle_http_service_error,
    handle_request_validation_error,
)
from .exceptions import ServiceException
from .http import ControllerBase

__all__ = [
    "Builder",
    "Environment",
]

D = TypeVar("D")


class Environment(Enum):
    DEVELOPMENT = 0
    PRODUCTION = 1


class Builder:
    def __init__(self):
        self._environment = Environment.DEVELOPMENT
        self._debug = False
        self._title = "Qena shared lib"
        self._description = "Qena shared tools for microservice"
        self._version = "0.1.0"
        self._lifespan = None
        self._openapi_url = "/openapi.json"
        self._docs_url = "/docs"
        self._redoc_url = "/redoc"
        self._metrics_endpoint = None
        self._instrumentator = None
        self._routers = []
        self._container = Container()
        self._built = False

    def with_environment(self, environment: Environment) -> "Builder":
        match environment:
            case Environment.DEVELOPMENT:
                self._environment = Environment.DEVELOPMENT
                self._debug = True
            case Environment.PRODUCTION:
                self._environment = Environment.PRODUCTION
                self._debug = False
                self._openapi_url = None
                self._docs_url = None
                self._redoc_url = None

        return self

    def with_title(self, title: str) -> "Builder":
        self._title = title

        return self

    def with_description(self, description: str) -> "Builder":
        self._description = description

        return self

    def with_version(self, version: str) -> "Builder":
        self._version = version

        return self

    def with_lifespan(self, lifespan: Lifespan) -> "Builder":
        self._lifespan = lifespan

        return self

    def with_controllers(
        self, controllers: list[type[ControllerBase]]
    ) -> "Builder":
        for index, controller in enumerate(controllers):
            if not isinstance(controller, type) or not issubclass(
                controller, ControllerBase
            ):
                raise TypeError(
                    f"controller {index} is {type(ControllerBase)}, expected instance of type or subclass of `ControllerBase`"
                )

            self._container.register(
                service=ControllerBase,
                factory=controller,
                scope=Scope.singleton,
            )

        return self

    def with_routers(self, routers: list[APIRouter]) -> "Builder":
        if any(not isinstance(router, APIRouter) for router in routers):
            raise TypeError("some routers are not type `APIRouter`")

        self._routers.extend(routers)

        return self

    def with_singleton(
        self, service: type[D], factory=empty, instance=empty, **kwargs
    ) -> "Builder":
        self._container.register(
            service=service,
            factory=factory,
            instance=instance,
            scope=Scope.singleton,
            **kwargs,
        )

        return self

    def with_transient(
        self, service: type[D], factory=empty, **kwargs
    ) -> "Builder":
        self._container.register(
            service=service,
            factory=factory,
            scope=Scope.transient,
            **kwargs,
        )

        return self

    def with_metrics(self, endpoint: str = "/metrics") -> "Builder":
        self._metrics_endpoint = endpoint
        self._instrumentator = Instrumentator()

        return self

    def build(self) -> FastAPI:
        if self._built:
            raise RuntimeError("fastapi application aleady built")

        app = FastAPI(
            debug=self._debug,
            title=self._title,
            description=self._description,
            version=self._version,
            openapi_url=self._openapi_url,
            docs_url=self._docs_url,
            redoc_url=self._redoc_url,
            lifespan=self._lifespan,
        )
        app.state.container = self._container

        app.exception_handler(ServiceException)(handle_http_service_error)
        app.exception_handler(RequestValidationError)(
            handle_request_validation_error
        )
        app.exception_handler(Exception)(handle_general_http_exception)

        self._resolve_api_controllers(app)

        if self._instrumentator is not None:
            self._instrumentator.instrument(app).expose(
                app=app,
                endpoint=self._metrics_endpoint or "/metrics",
                include_in_schema=False,
            )

        self._built = True

        return app

    def _resolve_api_controllers(self, app: FastAPI):
        api_controller_routers = [
            api_controller.register_route_handlers()
            for api_controller in self._container.resolve_all(ControllerBase)
        ]

        for router in self._routers + api_controller_routers:
            app.include_router(router)

    @property
    def environment(self) -> Environment:
        return self._environment

    @property
    def container(self) -> Container:
        return self._container
