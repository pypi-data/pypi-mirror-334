try:
    from typing import Optional
    import threading
    import sys
    import os
    from loguru import logger
except:
    logger = None

LOGURU_CONFIG = {
    "console": {
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] <cyan>{name}</cyan>:<cyan>{line}</cyan> <level>{message}</level>",
        "level": "INFO",
    },
    "file": {
        "rotation": "50 MB",
        "retention": "90 days",
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {name}:{function}:{line} {message}",
    },
}


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
        logger.remove()

        logger.add(
            sys.stdout,
            format=LOGURU_CONFIG["console"]["format"],
            level=LOGURU_CONFIG["console"]["level"],
            enqueue=True,
            filter=lambda record: record["extra"].get("name") == self.name
        )

        if log_path:
            self._file_handler = logger.add(
                log_path,
                rotation=LOGURU_CONFIG["file"]["rotation"],
                retention=LOGURU_CONFIG["file"]["retention"],
                level=LOGURU_CONFIG["file"]["level"],
                format=LOGURU_CONFIG["file"]["format"],
                enqueue=True,
                compression="zip",
                filter=lambda record: record["extra"].get("name") == self.name
            )

    @property
    def logger(self):
        return logger.bind(name=self.name)


def get_Logger(name: str, log_path: str=None):
    return LoggerFactory(name=name, log_path=log_path).logger