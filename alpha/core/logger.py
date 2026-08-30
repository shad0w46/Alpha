import logging
from pathlib import Path


def setup_logger(
    level="INFO",
    log_file="logs/alpha.log"
):

    Path(log_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(
        "alpha"
    )

    logger.setLevel(
        getattr(
            logging,
            str(level).upper(),
            logging.INFO
        )
    )

    logger.propagate = False

    # Avoid duplicate handlers when
    # Alpha is initialized more than once.
    if logger.handlers:

        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter
    )

    file_handler = logging.FileHandler(
        log_file
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.addHandler(
        file_handler
    )

    return logger
