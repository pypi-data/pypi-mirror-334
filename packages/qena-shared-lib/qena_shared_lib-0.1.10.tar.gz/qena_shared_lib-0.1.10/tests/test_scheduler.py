from datetime import datetime, timedelta
from typing import Annotated

from pytest import raises

from qena_shared_lib.dependencies.miscellaneous import DependsOn
from qena_shared_lib.scheduler import (
    ScheduleManager,
    Scheduler,
    SchedulerBase,
    schedule,
    scheduler,
)


def test_schedueler_scheduled_task(logstash):
    scheduler = Scheduler()

    @scheduler.schedule("* * * * *")
    def schedule_for_every_minute():
        pass

    schedule_manager = ScheduleManager(logstash=logstash)

    schedule_manager.include_scheduler(scheduler)

    scheduler_start = datetime.now()
    scheduler_end = datetime.now() + timedelta(
        seconds=schedule_manager.next_run_in
    )

    assert (scheduler_end - scheduler_start).seconds <= 60


def test_schedueler_class_based_scheduled_task(logstash):
    @scheduler()
    class TestScheduler(SchedulerBase):
        @schedule("* * * * *")
        def schedule_for_every_minute(self):
            pass

    schedule_manager = ScheduleManager(logstash=logstash)

    schedule_manager.include_scheduler(TestScheduler)
    schedule_manager.use_schedulers()

    scheduler_start = datetime.now()
    scheduler_end = datetime.now() + timedelta(
        seconds=schedule_manager.next_run_in
    )

    assert schedule_manager.scheduled_task_count == 1
    assert (scheduler_end - scheduler_start).seconds <= 60


def test_schedueler_scheduled_task_wrong_parameter():
    scheduler = Scheduler()

    with raises(TypeError) as exception_info:

        @scheduler.schedule("* * * * *")
        def schedule_for_every_minute(arg_one: dict):
            pass

    assert (
        str(exception_info.value)
        == "scheduler parament annotation for `arg_one` not valid, expected `Annotated[type, DependsOn(type)]`"
    )


def test_schedueler_class_based_scheduled_task_wrong_parameter(logstash):
    @scheduler()
    class TestScheduler(SchedulerBase):
        @schedule("* * * * *")
        def schedule_for_every_minute(self, arg_one: dict):
            pass

    schedule_manager = ScheduleManager(logstash=logstash)

    schedule_manager.include_scheduler(TestScheduler)

    with raises(TypeError) as exception_info:
        schedule_manager.use_schedulers()

    assert (
        str(exception_info.value)
        == "scheduler parament annotation for `arg_one` not valid, expected `Annotated[type, DependsOn(type)]`"
    )


def test_scheduler_scheduled_tasks_parameters():
    scheduler = Scheduler()

    @scheduler.schedule("* * * * *")
    def schedule_for_every_minute(
        arg_one: Annotated[dict, DependsOn(dict)],
        arg_two: Annotated[set, DependsOn(set)],
    ):
        pass

    *_, scheduled_task = scheduler.scheduled_tasks

    assert scheduled_task.parameters == {"arg_one": dict, "arg_two": set}
