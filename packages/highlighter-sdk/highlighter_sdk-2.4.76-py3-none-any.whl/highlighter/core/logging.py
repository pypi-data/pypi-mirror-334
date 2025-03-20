import logging
import os

__all__ = ["get_default_logger", "LOG"]


def get_default_logger(name):
    # https://stackoverflow.com/questions/43109355/logging-setlevel-is-being-ignored
    logging.debug(f"Setting up logging for logger={name}")
    logger = logging.getLogger(name)
    logger.setLevel(level=os.environ.get("LOG_LEVEL", "INFO"))
    return logger


class ColourStr:
    HEADER = "\033[95m"

    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    RED = "\033[91m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    RESET = "\033[0m"

    @staticmethod
    def blue(s):
        return ColourStr.BLUE + s + ColourStr.RESET

    @staticmethod
    def cyan(s):
        return ColourStr.CYAN + s + ColourStr.RESET

    @staticmethod
    def green(s):
        return ColourStr.GREEN + s + ColourStr.RESET

    @staticmethod
    def red(s):
        return ColourStr.RED + s + ColourStr.RESET

    @staticmethod
    def bold(s):
        return ColourStr.BOLD + s + ColourStr.RESET

    @staticmethod
    def underline(s):
        return ColourStr.UNDERLINE + s + ColourStr.RESET


LOG = get_default_logger("hl_client")
