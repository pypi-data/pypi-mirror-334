from repli.callback import Callback, NativeFunction, Subprocess
from typing import Any, Callable, Dict, List, Self, Type, Union


RESERVED_NAMES: List[str] = ["e", "q"]


class Command:
    def __init__(self, name: str, description: str, callback: Callback) -> None:
        self._name: str = name
        self._description: str = description
        self._callback: Callback = callback

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def callback(self) -> Callback:
        return self._callback


class Page:
    def __init__(self, name: str, description: str) -> None:
        self._name: str = name
        self._description: str = description
        self._commands: Dict[str, Union[Command, Self]] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def commands(self) -> Dict[str, Union[Command, Self]]:
        return self._commands

    def validate(self, name: str) -> None:
        if name in self.commands:
            raise ValueError(
                f"page or command with name '{name}' already exists in current page"
            )
        if name in RESERVED_NAMES:
            raise ValueError(f"page or command name '{name}' is reserved")

    def command(self, type: Type, name: str, description: str) -> Callable:
        self.validate(name)

        def decorator(callable: Callable[[str, str], Any]) -> None:
            callback: Callback
            if type == NativeFunction:
                callback = NativeFunction(callable=callable)
            elif type == Subprocess:
                callback = Subprocess(callable=callable)
            else:
                raise ValueError("invalid callback type")
            command = Command(name=name, description=description, callback=callback)
            self.commands[name] = command

        return decorator

    def add_page(self, page: Self) -> None:
        self.validate(page.name)
        self.commands[page.name] = page
