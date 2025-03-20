import rich.console


class Console(rich.console.Console):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Console, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def info(self, message: str) -> None:
        self.print(f"info: {message}", style="magenta", markup=False)

    def error(self, message: str) -> None:
        self.print(f"error: {message}", style="yellow", markup=False)
