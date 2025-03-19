from rich.console import Console


PREFIX: str = '[repli]'
INFO_PREFIX: str = 'info:'
ERROR_PREFIX: str = 'error:'


class Printer(Console):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Printer, cls).__new__(cls)
        return cls._instance

    def info(self, message: str) -> None:
        self.print(f'{PREFIX} {INFO_PREFIX} {message}', style='magenta', markup=False)

    def error(self, message: str) -> None:
        self.print(f'{PREFIX} {ERROR_PREFIX} {message}', style='yellow', markup=False)
