from repli.callback import Callback, NativeFunction, Subprocess
from typing import Any, Callable, Dict, List, Self, Type, Union


RESERVED_NAMES: List[str] = ["e", "q"]


class Command:
    def __init__(self, description: str, callback: Callback) -> None:
        self._description: str = description
        self._callback: Callback = callback

    @property
    def description(self) -> str:
        return self._description

    @property
    def callback(self) -> Callback:
        return self._callback


class Page:
    def __init__(self, description: str) -> None:
        self._description: str = description
        self._commands: Dict[str, Union[Command, Self]] = {}
        self._index: int = 1

    @property
    def description(self) -> str:
        return self._description

    @property
    def commands(self) -> Dict[str, Union[Command, Self]]:
        return self._commands

    @property
    def index(self) -> int:
        return self._index

    def command(self, type: Type, description: str) -> Callable:
        def decorator(callable: Callable[[str, str], Any]) -> None:
            callback: Callback
            if type == NativeFunction:
                callback = NativeFunction(callable=callable)
            elif type == Subprocess:
                callback = Subprocess(callable=callable)
            else:
                raise ValueError("invalid callback type")
            command = Command(description=description, callback=callback)
            self.commands[str(self.index)] = command
            self._index += 1

        return decorator

    def add_page(self, page: Self) -> None:
        self.commands[str(self.index)] = page
        self._index += 1
