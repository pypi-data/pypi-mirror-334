import errno
import logging
import sys

from rich.console import Console
from rich.logging import RichHandler


class Console2(Console):
    # OSX will return EAGAIN while still writing a buffer to stdout, lol
    def _write_buffer(self) -> None:
        try:
            super()._write_buffer()  # type: ignore
        except BlockingIOError as e:
            if e.errno == errno.EAGAIN:
                pass


CONSOLE = Console2(stderr=True) if sys.platform == "darwin" else Console(stderr=True)
FORMAT = "%(message)s"
logging.basicConfig(
    level="ERROR",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=CONSOLE)],
)

log: logging.Logger = logging.getLogger("rich")


def set_verbosity(verbosity: int) -> None:
    lvl = logging.WARNING
    if verbosity == 1:
        lvl = logging.INFO
    elif verbosity > 1:
        lvl = logging.DEBUG
    log.setLevel(lvl)
