from repli.callback import Callback, NativeFunction, Subprocess
from typing import Callable, Dict, List, Optional, Self, Type, Union


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
    def __init__(
        self, name: str, description: str, commands: Dict[str, Union[Command, Self]]
    ) -> None:
        self._name: str = name
        self._description: str = description
        self._commands: Dict[str, Union[Command, Self]] = commands

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def commands(self) -> Dict[str, Union[Command, Self]]:
        return self._commands


class PageFactory:
    def __init__(self) -> None:
        self._commands: Dict[str, Union[Command, Page]] = {}

    @property
    def commands(self) -> Dict[str, Union[Command, Page]]:
        return self._commands

    def get(self, name: str, description: str) -> Page:
        return Page(name=name, description=description, commands=self.commands)

    def validate(self, name: str) -> None:
        if name in self.commands:
            raise ValueError(
                f"page or command with name '{name}' already exists in current page"
            )
        if name in RESERVED_NAMES:
            raise ValueError(f"page or command name '{name}' is reserved")

    def command(self, type: Type, name: str, description: str) -> Callable:
        self.validate(name)

        def decorator(callable: Callable[[str, str], Callback]) -> None:
            if type == NativeFunction:
                callback = NativeFunction(callable=callable)
            elif type == Subprocess:
                callback = Subprocess(callable=callable)
            else:
                raise ValueError("invalid callback type")
            command = Command(name=name, description=description, callback=callback)
            self.commands[name] = command

        return decorator

    def add_page(self, page: Page) -> None:
        self.validate(page.name)
        self.commands[page.name] = page
