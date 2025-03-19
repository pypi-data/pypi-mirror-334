from rich.console import Console as C
from rich.text import Text


class Console:
    def __init__(self):
        self.console = C()

    def print(self, text):
        self.console.print(text)

    def print_error(self, text):
        self.console.print(Text(text, style="bold red"))

    def print_success(self, text):
        self.console.print(Text(text, style="bold green"))

    def print_warning(self, text):
        self.console.print(Text(text, style="bold yellow"))
