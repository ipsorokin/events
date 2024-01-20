from typing import TypeVar, Callable

from events import Event, event

_T = TypeVar('_T')


class ObservableCollection(list[_T]):
    def __init__(self):
        super().__init__()
        self.on_changed: Event[Callable[[_T, str], None]] = Event()

    def append(self, __object: _T):
        super().append(__object)
        self.on_changed(__object, "append")

    def remove(self, __value: _T):
        super().remove(__value)
        self.on_changed(__value, "remove")


def use_class():
    """

    Output:
        use_class-append=	FirstElement
        use_class-append:	FirstElement
        use_class-append=	LastElement
        use_class-append:	LastElement
        use_class-remove=	FirstElement
    """
    collection = ObservableCollection[str]()

    def _function(obj, action):
        print(f"use_class-{action}:\t{obj}")

    collection.on_changed += lambda obj, action: print(f"use_class-{action}=\t{obj}")
    collection.on_changed += _function
    collection.append("FirstElement")
    collection.append("LastElement")
    collection.on_changed -= _function
    collection.remove("FirstElement")


def use_decorator():
    """

    Output
        use_decorator-append:	FirstElement
        use_decorator-append:	LastElement
        use_decorator-remove:	FirstElement
    """
    collection = ObservableCollection[str]()

    @event.add(collection, 'on_changed')
    def event_handler(obj, action):
        print(f"use_decorator-{action}:\t{obj}")

    collection.append("FirstElement")
    collection.append("LastElement")
    collection.remove("FirstElement")


if __name__ == "__main__":
    use_class()
    use_decorator()
