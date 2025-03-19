from asyncio import AbstractEventLoop, get_running_loop

from pydantic import TypeAdapter

__all__ = ["AsyncEventLoopMixin", "TypeAdapterCache"]

ABSTRACT_EVENT_LOOP_ATTRIBUTE = "__abstract_event_loop__"


class AsyncEventLoopMixin:
    @property
    def loop(self) -> AbstractEventLoop:
        previous_running_loop = getattr(
            self, ABSTRACT_EVENT_LOOP_ATTRIBUTE, None
        )
        current_running_loop = None

        try:
            current_running_loop = get_running_loop()
        except RuntimeError:
            if previous_running_loop is None:
                raise

        if previous_running_loop is None or (
            current_running_loop is not None
            and previous_running_loop != current_running_loop
        ):
            setattr(self, ABSTRACT_EVENT_LOOP_ATTRIBUTE, current_running_loop)

        return getattr(self, ABSTRACT_EVENT_LOOP_ATTRIBUTE)


class TypeAdapterCache:
    _cache = {}

    @classmethod
    def cache_annotation(cls, annotation: type):
        if annotation not in cls._cache:
            cls._cache[annotation] = TypeAdapter(annotation)

    @classmethod
    def get_type_adapter(cls, annotation: type) -> TypeAdapter:
        cls.cache_annotation(annotation)

        return cls._cache[annotation]
