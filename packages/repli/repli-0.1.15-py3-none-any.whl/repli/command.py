from repli.callback import Callback


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
