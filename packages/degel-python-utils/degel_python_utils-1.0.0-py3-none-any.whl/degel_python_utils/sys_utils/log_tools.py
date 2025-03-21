"""Custom log formatting."""

import contextvars
import logging
import time
from typing import Any, Literal, Self, Union, cast

from blessings import Terminal


def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Set up and return a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = OurLogHandler()
    handler.setFormatter(OurLogFormatter())
    logger.addHandler(handler)
    return logger


log_prefix: contextvars.ContextVar[str] = contextvars.ContextVar(
    "log_prefix", default=""
)


class OurLogger(logging.Logger):
    """Add some extra logging levels."""

    MINOR = logging.INFO - 5
    MAJOR = logging.WARNING - 5

    logging.addLevelName(MINOR, "MINOR")
    logging.addLevelName(MAJOR, "MAJOR")

    def minor(self: Self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log level MINOR."""
        if self.isEnabledFor(self.MINOR):
            self._log(self.MINOR, message, args, **kwargs)

    def major(self: Self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log level MAJOR."""
        if self.isEnabledFor(self.MAJOR):
            self._log(self.MAJOR, message, args, **kwargs)


logging.setLoggerClass(OurLogger)


class OurLogFormatter(logging.Formatter):
    """Apply colors to the different logging levels."""

    def __init__(
        self: Self,
        fmt: str = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        use_color: bool = True,
    ) -> None:
        """Initialize the logger."""
        super().__init__(fmt, datefmt, style)
        self.use_color = use_color
        self.t = Terminal() if use_color else None

    def format(self: Self, record: logging.LogRecord) -> str:
        """Format a log line."""
        ct = self.converter(record.created)
        prefix = log_prefix.get()
        record.msg = f"{prefix}{record.msg}"
        record.asctime = (
            f"{time.strftime('%Y-%m-%d %H:%M:%S', ct)},{int(record.msecs):03}"
        )
        if self.use_color and self.t is not None:
            color = self.get_color(record.levelno)
            level = f"{record.levelname+':':<10}"
            record.levelname = f"{color}{level}{self.t.normal}"
            record.msg = f"{color}{record.msg}{self.t.normal}"

        formatted_msg = super().format(record)
        if "\n" in record.msg:
            lines = formatted_msg.split("\n")
            space_prefix_length = len(record.asctime) + len(level) + 5
            space_prefix = " " * space_prefix_length
            if self.use_color and self.t is not None:
                colored_lines = [lines[0]] + [
                    f"{color}{space_prefix}{line}{self.t.normal}" for line in lines[1:]
                ]
                return "\n".join(colored_lines)
            return formatted_msg
        return formatted_msg

    def get_color(self: Self, levelno: int) -> str:
        """Map log levels to colors."""
        if not self.t:
            return ""
        return {
            logging.DEBUG: self.t.red + self.t.bold,
            OurLogger.MINOR: self.t.yellow,
            logging.INFO: self.t.blue,
            OurLogger.MAJOR: self.t.magenta,
            logging.WARNING: self.t.yellow,
            logging.ERROR: self.t.red,
            logging.CRITICAL: self.t.red,
        }.get(levelno, self.t.normal)

    def formatException(self: Self, ei: Union[Exception, tuple]) -> str:
        """Highlight exception lines."""
        if self.use_color and self.t is not None:
            return self.t.red + super().formatException(cast(tuple, ei)) + self.t.normal
        return super().formatException(cast(tuple, ei))


class OurLogHandler(logging.StreamHandler):
    """Auto-exit the app if it hits a critical error."""

    def emit(self: Self, record: logging.LogRecord) -> None:
        """Exit application if writing a CRITICAL log line."""
        if record.levelno >= logging.CRITICAL:
            raise RuntimeError("Exit forced by our logging handler")
        super().emit(record)
