from typing import TypeVar, Callable, Generic

EventHandler = TypeVar('EventHandler', bound=Callable)


class Event(Generic[EventHandler]):
    def __init__(self):
        self.__handlers: list[EventHandler] = []

    def __iadd__(self, other: EventHandler):
        self.add(other)
        return self

    def __isub__(self, other: EventHandler):
        self.remove(other)
        return self

    def __call__(self, *args, **kwargs):
        if self.__handlers:
            for handler in self.__handlers:
                handler(*args, **kwargs)

    def add(self, other: EventHandler):
        self.__handlers.append(other)

    def remove(self, other: EventHandler):
        if other in self.__handlers:
            self.__handlers.remove(other)


class event:
    @staticmethod
    def add(_instance, _event):
        if not hasattr(_instance, _event):
            raise AttributeError

        def decorator(func):
            attr = getattr(_instance, _event)
            attr.add(func)

        return decorator
