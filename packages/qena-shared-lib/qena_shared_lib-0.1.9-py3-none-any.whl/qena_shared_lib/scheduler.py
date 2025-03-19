from asyncio import Future, Task, iscoroutinefunction, sleep
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from importlib import import_module
from inspect import signature
from os import name as osname
from typing import Any, Callable, TypeVar
from zoneinfo import ZoneInfo

from cronsim import CronSim
from prometheus_client import Enum as PrometheusEnum
from punq import Container, Scope

from .dependencies.miscellaneous import validate_annotation
from .logging import LoggerProvider
from .logstash import BaseLogstashSender
from .utils import AsyncEventLoopMixin

__all__ = [
    "schedule",
    "ScheduleManager",
    "scheduler",
    "Scheduler",
    "SchedulerBase",
]

S = TypeVar("S")
SCHEDULER_ATTRIBUTE = "__scheduler__"
SCHEDULED_TASK_ATTRIBUTE = "__scheduled_task__"


@dataclass
class ScheduledTask:
    task: Callable
    cron_expression: str
    zone_info: ZoneInfo | None

    def __post_init__(self):
        self._next_run_in = None
        self._ran = False
        self._paramters = {}

        for parameter_name, paramter in signature(self.task).parameters.items():
            dependency = validate_annotation(paramter.annotation)

            if dependency is None:
                raise TypeError(
                    f"scheduler parament annotation for `{parameter_name}` not valid, expected `Annotated[type, DependsOn(type)]`"
                )

            self._paramters[parameter_name] = dependency

    @property
    def next_run_in(self) -> int | None:
        return self._next_run_in

    @next_run_in.setter
    def next_run_in(self, value: int):
        self._next_run_in = value

    @property
    def ran(self) -> bool:
        return self._ran

    @ran.setter
    def ran(self, value: bool):
        self._ran = value

    @property
    def parameters(self) -> dict[str, type]:
        return self._paramters


class Scheduler:
    def __init__(self):
        self._scheduled_tasks: list[ScheduledTask] = []

    def schedule(
        self, cron_expression: str, timezone: str | None = None
    ) -> Callable[[Callable], Callable]:
        def wrapper(task: Callable) -> Callable:
            self.add_task(
                task=task, cron_expression=cron_expression, timezone=timezone
            )

            return task

        return wrapper

    def add_task(
        self, task: Callable, cron_expression: str, timezone: str | None
    ):
        self._scheduled_tasks.append(
            ScheduledTask(
                task=task,
                cron_expression=cron_expression,
                zone_info=ZoneInfo(timezone) if timezone is not None else None,
            )
        )

    def __call__(self, scheduler: type[S]) -> type[S]:
        setattr(scheduler, SCHEDULER_ATTRIBUTE, self)

        return scheduler

    @property
    def scheduled_tasks(self) -> list[ScheduledTask]:
        return self._scheduled_tasks


def scheduler() -> Scheduler:
    return Scheduler()


@dataclass
class ScheduledTaskMeta:
    cron_expression: str
    timezone: str | None = None


def schedule(
    cron_expression: str, *, timezone: str | None = None
) -> Callable[[Callable], Callable]:
    def wrapper(task: Callable) -> Callable:
        setattr(
            task,
            SCHEDULED_TASK_ATTRIBUTE,
            ScheduledTaskMeta(
                cron_expression=cron_expression, timezone=timezone
            ),
        )

        return task

    return wrapper


class SchedulerBase:
    def get_scheduler(self) -> Scheduler:
        scheduler = getattr(self, SCHEDULER_ATTRIBUTE, None)

        if scheduler is None or not isinstance(scheduler, Scheduler):
            raise TypeError(
                f"{self.__class__.__name__} not a scheduler, possibly no annotated with either `Scheduler`"
            )

        return scheduler

    def register_scheduled_tasks(self) -> Scheduler:
        scheduler = self.get_scheduler()

        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name, None)

            if attribute is None:
                continue

            scheduled_task_meta = getattr(
                attribute, SCHEDULED_TASK_ATTRIBUTE, None
            )

            if scheduled_task_meta is None:
                continue

            if not isinstance(scheduled_task_meta, ScheduledTaskMeta):
                raise TypeError(
                    f"expected `{SCHEDULED_TASK_ATTRIBUTE}` to by of type `ScheduledTaskMeta`, got {type(scheduled_task_meta)}"
                )

            scheduler.add_task(
                task=attribute,
                cron_expression=scheduled_task_meta.cron_expression,
                timezone=scheduled_task_meta.timezone,
            )

        return scheduler


class ScheduleManager(AsyncEventLoopMixin):
    SCHEDULE_MANAGER_STATE = PrometheusEnum(
        name="schedule_manager_state",
        documentation="Schedule manager state",
        states=["running", "stopped"],
    )

    def __init__(
        self,
        logstash: BaseLogstashSender,
        container: Container | None = None,
    ):
        self._container = container or Container()
        self._logstash = logstash
        self._scheduled_tasks: list[ScheduledTask] = []
        self._next_run_in = None
        self._scheduler_task = None
        self._logger = LoggerProvider.default().get_logger("schedule_manager")

    def include_scheduler(self, scheduler: Scheduler | type[SchedulerBase]):
        if isinstance(scheduler, Scheduler):
            self._scheduled_tasks.extend(scheduler.scheduled_tasks)

            return

        if isinstance(scheduler, type) and issubclass(scheduler, SchedulerBase):
            self._container.register(
                service=SchedulerBase,
                factory=scheduler,
                scope=Scope.singleton,
            )

            return

        raise TypeError(
            f"scheduler is {type(scheduler)}, expected instance of type or subclass of `Scheduler` or `type[SchedulerBase]`"
        )

    @property
    def container(self) -> Container:
        return self._container

    @property
    def next_run_in(self) -> int:
        self._calculate_next_schedule()

        return self._next_run_in or 0

    @property
    def scheduled_task_count(self) -> int:
        return len(self._scheduled_tasks)

    def start(self):
        if not self._aquired_lock():
            return

        if self._scheduler_task is not None and not self._scheduler_task.done():
            raise RuntimeError("scheduler already running")

        self.use_schedulers()
        self._logger.info(
            "schedule manager started for %d %s",
            self.scheduled_task_count,
            "tasks" if self.scheduled_task_count > 1 else "task",
        )

        if self.scheduled_task_count == 0:
            return

        self._scheduler_task = self.loop.create_task(self._run_scheduler())

        self._scheduler_task.add_done_callback(self._on_scheduler_done)
        self.SCHEDULE_MANAGER_STATE.state("running")

    def use_schedulers(self):
        for scheduler in [
            scheduler.register_scheduled_tasks()
            for scheduler in self._container.resolve_all(SchedulerBase)
        ]:
            self._scheduled_tasks.extend(scheduler.scheduled_tasks)

    def stop(self):
        if self._scheduler_task is not None and not self._scheduler_task.done():
            self._scheduler_task.cancel()

        self.SCHEDULE_MANAGER_STATE.state("stopped")

    def _on_scheduler_done(self, task: Task):
        if task.cancelled():
            return

        exception = task.exception()

        if exception is not None:
            self._logstash.error(
                message="error occured in schedule manager",
                exception=exception,
            )

            return

        self._logger.info("schedule manager stopping")

    def _aquired_lock(self) -> bool:
        if osname != "posix":
            self._logger.warning("lock not supported in %s", osname)

            return False

        try:
            fcntl = import_module("fcntl")
            lockf = fcntl.lockf
            LOCK_EX = fcntl.LOCK_EX
            LOCK_NB = fcntl.LOCK_NB

            self._fd = open(file="scheduler.lock", mode="w+", encoding="utf-8")

            lockf(self._fd, LOCK_EX | LOCK_NB)
        except OSError:
            self._logger.warning("a schedule manager already running")

            return False
        except ModuleNotFoundError:
            self._logger.exception("module `fcntl` no found")

            return False

        return True

    async def _run_scheduler(self):
        while True:
            self._calculate_next_schedule()
            self._logger.debug(
                "next tasks will be executed after `%d` seconds",
                self._next_run_in or 0,
            )

            await sleep(self._next_run_in or 0)
            self._logger.debug(
                "executing tasks after `%d` seconds since last execution",
                self.next_run_in or 0,
            )

            for scheduled_task in self._scheduled_tasks:
                next_run_in_diff = abs(
                    (self._next_run_in or 0) - (scheduled_task.next_run_in or 0)
                )

                if next_run_in_diff > 60:
                    continue

                args = self._resolve_dependencies(scheduled_task)

                if iscoroutinefunction(scheduled_task.task):
                    self.loop.create_task(
                        scheduled_task.task(**args)
                    ).add_done_callback(self._on_task_done)
                else:
                    self.loop.run_in_executor(
                        executor=None, func=scheduled_task.task
                    ).add_done_callback(partial(self._on_task_done, **args))

                scheduled_task.ran = True

    def _resolve_dependencies(
        self, scheduled_task: ScheduledTask
    ) -> dict[str, Any]:
        args = {}

        if self._container is None:
            return args

        for parameter_name, dependency in scheduled_task.parameters.items():
            args[parameter_name] = self._container.resolve(dependency)

        return args

    def _on_task_done(self, task_or_future: Task | Future):
        if task_or_future.cancelled():
            return

        exception = task_or_future.exception()

        if exception is not None:
            self._logstash.error(
                message="error occured while executing task",
                exception=exception,
            )

    def _calculate_next_schedule(self):
        prev_run_in = self._next_run_in or 0
        self._next_run_in = None

        for scheduled_task in self._scheduled_tasks:
            if (
                not scheduled_task.ran
                and scheduled_task.next_run_in is not None
            ):
                scheduled_task.next_run_in = (
                    scheduled_task.next_run_in - prev_run_in
                )

                if (
                    self._next_run_in is not None
                    and (scheduled_task.next_run_in or 0) < self._next_run_in
                ) or self._next_run_in is None:
                    self._next_run_in = scheduled_task.next_run_in

                continue

            current_datetime = datetime.now(tz=scheduled_task.zone_info)
            next_datetime = next(
                CronSim(
                    expr=scheduled_task.cron_expression,
                    dt=datetime.now(tz=scheduled_task.zone_info),
                )
            )
            next_run_in = (next_datetime - current_datetime).seconds

            if next_run_in == 0:
                continue

            if self._next_run_in is None or next_run_in < self._next_run_in:
                self._next_run_in = next_run_in

            scheduled_task.next_run_in = next_run_in
            scheduled_task.ran = False
