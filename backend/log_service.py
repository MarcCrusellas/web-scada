import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class LogService:
    def __init__(self, log_directory="logs", log_file="service.log", max_bytes=5 * 1024 * 1024, backup_count=3):
        self.log_directory = Path(log_directory)
        self.log_directory.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_directory / log_file

        # Configure the logger
        self.logger = logging.getLogger("WebSCADA")
        self.logger.setLevel(logging.DEBUG)

        # Create a rotating file handler
        handler = RotatingFileHandler(self.log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

# Example usage
if __name__ == "__main__":
    log_service = LogService()
    log_service.log_info("This is an info message.")
    log_service.log_warning("This is a warning message.")
    log_service.log_error("This is an error message.")
    log_service.log_debug("This is a debug message.")
