import rich.console


PREFIX: str = "[repli]"
INFO_PREFIX: str = "info:"
ERROR_PREFIX: str = "error:"


class Console(rich.console.Console):
    def info(self, message: str) -> None:
        self.print(f"{PREFIX} {INFO_PREFIX} {message}", style="magenta", markup=False)

    def error(self, message: str) -> None:
        self.print(f"{PREFIX} {ERROR_PREFIX} {message}", style="yellow", markup=False)
