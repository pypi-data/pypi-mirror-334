import os
ENVIRONMENT = "local"

# PROJECT_ROOT = os.path.abspath(os.path.join("../.."))
PROJECT_ROOT = "."
OUTPUTS_PATH = "outputs"
DATA_PATH = "data"

LOG_CONFIG = {
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
