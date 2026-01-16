import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


class LogConfig:
    """Centralized logging configuration for MedKit.

    Logs are stored in user's home directory for:
    - HIPAA compliance (separate from source code)
    - Privacy (each user has isolated logs)
    - Clean development (no logs cluttering repo)
    - Production readiness (industry standard)

    Log directory: ~/.medkit/logs/
    """

    # Log directory in user's home
    LOG_DIR = Path.home() / '.medkit' / 'logs'

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Log file paths
    MAIN_LOG = LOG_DIR / 'medkit.log'
    CLI_LOG = LOG_DIR / 'cli.log'
    API_LOG = LOG_DIR / 'api.log'
    ERROR_LOG = LOG_DIR / 'errors.log'

    # Logging configuration
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    # Log rotation settings
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5  # Keep 5 rotated logs

    # Log levels
    DEFAULT_LEVEL = logging.INFO
    CLI_LEVEL = logging.INFO
    API_LEVEL = logging.DEBUG
    ERROR_LEVEL = logging.ERROR

    @classmethod
    def get_logger(cls, name: str, log_file: Path = None, level: int = None) -> logging.Logger:
        """
        Get a configured logger for the given name.

        Args:
            name: Logger name (typically module name)
            log_file: Optional specific log file (defaults to MAIN_LOG)
            level: Optional log level (defaults to DEFAULT_LEVEL)

        Returns:
            Configured logging.Logger instance
        """
        logger = logging.getLogger(name)

        if logger.handlers:  # Logger already configured
            return logger

        log_file = log_file or cls.MAIN_LOG
        level = level or cls.DEFAULT_LEVEL

        logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(cls.LOG_FORMAT, datefmt=cls.DATE_FORMAT)

        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=cls.MAX_LOG_SIZE,
            backupCount=cls.BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        return logger

    @classmethod
    def cleanup_old_logs(cls, days: int = 30) -> None:
        """
        Remove log files older than specified days.

        Args:
            days: Number of days to keep (default 30)
        """
        import time

        now = time.time()
        cutoff = now - (days * 86400)  # seconds in a day

        for log_file in cls.LOG_DIR.glob('**/*.log*'):
            if log_file.stat().st_mtime < cutoff:
                try:
                    log_file.unlink()
                except Exception as e:
                    print(f"Warning: Could not delete {log_file}: {e}")


class PrivacyConfig:
    """Privacy configuration constants."""

    # Data retention periods (days)
    CHAT_HISTORY_RETENTION_DAYS = 365
    AUDIT_LOG_RETENTION_DAYS = 2555  # 7 years for HIPAA
    ASSESSMENT_RETENTION_DAYS = 2555  # 7 years

    # Storage paths
    STORAGE_DIR = Path(__file__).parent / "secure_storage"
    SESSIONS_DIR = STORAGE_DIR / "sessions"
    AUDIT_LOGS_DIR = STORAGE_DIR / "audit_logs"
    CONSENT_DIR = STORAGE_DIR / "consents"

    # Logging flags
    LOG_DATA_ACCESS = True
    LOG_DATA_MODIFICATIONS = True
    LOG_DATA_DELETIONS = True
