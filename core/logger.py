import logging


def setup_logger(logger):
    """Configure logging format and output."""
    handler = logging.FileHandler("test_logs.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


