from ..constants import LOG_CONFIG
try:
    from typing import Optional
    import threading
    import sys
    import os
    from loguru import logger
except:
    logger = None


class LoggerFactory:
    _instances = {}
    _lock = threading.RLock()

    def __new__(cls, name: str = "global", log_path: Optional[str] = None):
        if name not in cls._instances:
            with cls._lock:
                if name not in cls._instances:
                    cls._instances[name] = super().__new__(cls)
                    cls._instances[name]._initialized = False
        return cls._instances[name]

    def __init__(self, name: str = "global", log_path: Optional[str] = None):
        if not getattr(self, '_initialized', False):
            self.name = name
            self._setup_logger(log_path)
            self._initialized = True

    def _setup_logger(self, log_path: Optional[str] = None):
        if logger:
            logger.remove()

            logger.add(
                sys.stdout,
                format=LOG_CONFIG["console"]["format"],
                level=LOG_CONFIG["console"]["level"],
                enqueue=True,
                filter=lambda record: record["extra"].get("name") == self.name
            )

            if log_path:
                self._file_handler = logger.add(
                    log_path,
                    rotation=LOG_CONFIG["file"]["rotation"],
                    retention=LOG_CONFIG["file"]["retention"],
                    level=LOG_CONFIG["file"]["level"],
                    format=LOG_CONFIG["file"]["format"],
                    enqueue=True,
                    compression="zip",
                    filter=lambda record: record["extra"].get("name") == self.name
                )

    @property
    def logger(self):
        if logger:
            return logger.bind(name=self.name)


def get_logger(name: str, log_path: str=None):
    return LoggerFactory(name=name, log_path=log_path).logger