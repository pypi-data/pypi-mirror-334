from time import sleep

from rich.columns import Columns
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS


class WaitingWidget:

    def __init__(self):
        self.live = Live(
            Spinner("dots", text=Text("Starting", style="green")), refresh_per_second=10
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.live.stop()

    def update_text(self, text):
        self.live.renderable.update(text=Text(text, style="green"))


def make_waiting_widget():

    return WaitingWidget()


def v2():
    # need to be a context manager?
    with make_waiting_widget() as widget:
        for i in range(40):
            if i < 20:
                current_status = "PENDING"
            else:
                current_status = "RUNNING"
            text = f"Waiting job to finish, current status {current_status} (waited for {i}s)"
            widget.update_text(text)
            sleep(0.1)


def v1():
    spinner_name = "dots"
    current_status = "PENDING"
    text = f"Waiting job to finish, current status {current_status}"
    with Live(
        Spinner(spinner_name, text=Text(text, style="green")), refresh_per_second=10
    ) as live:
        for i in range(40):
            if i < 20:
                current_status = "PENDING"
            else:
                current_status = "RUNNING"
            text = f"Waiting job to finish, current status {current_status} (waited for {i}s)"
            live.renderable.update(text=Text(text, style="green"))
            sleep(0.1)


# v1()
v2()
