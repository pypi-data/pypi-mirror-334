import abc
import subprocess
import shlex
from repli import console
from rich.rule import Rule
from typing import Callable


class Callback(abc.ABC):
    def __init__(self) -> None:
        pass

    def __call__(self, *args: str, **kwargs: str) -> bool:
        console.info(f"callback function args: {args}")
        console.info(f"callback function kwargs: {kwargs}")
        return False


class NativeFunction(Callback):
    def __init__(
        self,
        callable: Callable[[str, str], None],
    ) -> None:
        super().__init__()
        self._callable: Callable[[str, str], None] = callable

    @property
    def callable(self) -> Callable[[str, str], None]:
        return self._callable

    def __call__(self, *args: str, **kwargs: str) -> bool:
        super().__call__(*args, **kwargs)
        try:
            console.print(Rule(style="magenta"))
            self.callable(*args, **kwargs)
            console.print(Rule(style="magenta"))
        except Exception as e:
            console.error(f"native function raised an exception: {e}")
        finally:
            return False


class Subprocess(Callback):
    def __init__(
        self,
        callable: Callable[[str, str], str],
    ) -> None:
        super().__init__()
        self._callable: Callable[[str, str], str] = callable

    @property
    def callable(self) -> Callable[[str, str], str]:
        return self._callable

    def __call__(self, *args: str, **kwargs: str) -> bool:
        super().__call__(*args, **kwargs)
        arguments = self.callable(*args, **kwargs)
        console.info(f"running subprocess command: '{arguments}'")
        try:
            console.print(Rule(style="magenta"))
            returncode = subprocess.call(
                args=shlex.split(arguments),
                text=True,
                encoding="utf-8",
            )
            console.print(Rule(style="magenta"))
            if returncode != 0:
                console.error(f"subprocess returned an error code: {returncode}")
        except Exception as e:
            console.error(f"subprocess raised an exception: {e}")
        finally:
            return False
