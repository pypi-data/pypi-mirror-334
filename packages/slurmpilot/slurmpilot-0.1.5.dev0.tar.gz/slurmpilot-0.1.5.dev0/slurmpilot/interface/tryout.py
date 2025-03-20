import sys
import time


def print_statusline(msg: str):
    last_msg_length = len(getattr(print_statusline, "last_msg", ""))
    print(" " * last_msg_length, end="\r")
    print(msg, end="\r")
    # sys.stdout.flush()  # Some say they needed this, I didn't.
    setattr(print_statusline, "last_msg", msg)


for msg in ["Initializing...", "Initialization successful!"]:
    print_statusline(msg)
    time.sleep(1)
