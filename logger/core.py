import logging.config

from .exceptions import LoggerNotFoundException
from .settings import config_settings


def create_logger(logger_name: str) -> logging.getLogger:

    """
    Function to get logger.
    :param logger_name: you can see all loggers in logger.settings.py.
    :return: logger instance.
    """

    if logger_name not in config_settings['loggers'].keys():
        raise LoggerNotFoundException("Are you sure logger you use exists?")

    logging.config.dictConfig(config_settings)
    logger = logging.getLogger(logger_name)

    return logger
