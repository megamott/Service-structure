import logging
import sys


class Logger:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Logger, cls).__new__(cls)
            cls.instance._initialized = False
        return cls.instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        handler.setLevel(logging.DEBUG)
        self._logger.addHandler(handler)

        self._initialized = True

    def info(self, text):
        self._logger.info(text)

    def error(self, text):
        self._logger.error(text)
