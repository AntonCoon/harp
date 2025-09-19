import logging
from pathlib import Path

DEFAULT_LOG_FILE = Path(".harp.log")


def get_logger(
    name: str = "harp", log_file: Path = DEFAULT_LOG_FILE
) -> logging.Logger:
    """Return a configured logger that logs to file and console."""
    logger = logging.getLogger(name)
    if logger.handlers:  # already configured
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_fmt)

    logger.addHandler(file_handler)

    return logger
