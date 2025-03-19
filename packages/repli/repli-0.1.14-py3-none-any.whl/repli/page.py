from repli.callback import Callback, NativeFunction, Subprocess
from repli.command import Command
from typing import Callable, Dict, List, Optional, Self, Type, Union


RESERVED_NAMES: List[str] = ['e', 'q']


class Page:
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        self._name: str = name
        self._description: str = description
        self._commands: Dict[str, Union[Command, Self]] = {}

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def commands(self) -> Dict[str, Union[Command, Self]]:
        return self._commands
    
    def validate(self, name: str) -> None:
        if name in self._commands:
            raise ValueError(f'page or command with name \'{name}\' already exists in current page')
        if name in RESERVED_NAMES:
            raise ValueError(f'page or command name \'{name}\' is reserved')

    def command(self, type: Type, name: str, description: str) -> Callable:
        self.validate(name)
        def decorator(callable: Callable[[str, str], Callback]) -> None:
            if type == NativeFunction:
                callback = NativeFunction(callable=callable)
            elif type == Subprocess:
                callback = Subprocess(callable=callable)
            else:
                raise ValueError('invalid callback type')
            command = Command(name=name, description=description, callback=callback)
            self._commands[name] = command
        return decorator

    def add_page(self, page: Self, name: str, description: str) -> None:
        page.name = name
        page.description = description
        self.validate(name)
        self._commands[page.name] = page
