"""
Application Logging Configuration

Responsibilities:
- Configure console logging
- Configure application log file
- Configure error log file
- Configure log formatting
- Provide reusable logger instances
"""

from pathlib import Path
import logging
import logging.config

from Backend.app.core.configure import settings


# =============================================================================
# Create Logs Directory
# =============================================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Logging Configuration
# =============================================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },

    "handlers": {
        # ---------------------------------------------------------------------
        # Console Handler
        # ---------------------------------------------------------------------
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG" if settings.DEBUG else "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },

        # ---------------------------------------------------------------------
        # Application Log File
        # ---------------------------------------------------------------------
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": str(LOG_DIR / "app.log"),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "encoding": "utf-8",
        },

        # ---------------------------------------------------------------------
        # Error Log File
        # ---------------------------------------------------------------------
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "default",
            "filename": str(LOG_DIR / "error.log"),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },

    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "app_file",
            "error_file",
        ],
    },
}


# =============================================================================
# Setup Logging
# =============================================================================

def setup_logging() -> None:
    """
    Initialize the application's logging system.

    Call this once during application startup.
    """
    logging.config.dictConfig(LOGGING_CONFIG)


# =============================================================================
# Logger Factory
# =============================================================================

def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Example:
        logger = get_logger(__name__)

    Args:
        name: Module name.

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)