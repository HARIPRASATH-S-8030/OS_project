import logging
from config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class PolicyLogger:

    @staticmethod
    def info(message):
        logging.info(message)
        print("[INFO]", message)

    @staticmethod
    def warning(message):
        logging.warning(message)
        print("[WARNING]", message)

    @staticmethod
    def critical(message):
        logging.critical(message)
        print("[CRITICAL]", message)

