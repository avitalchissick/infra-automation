"""
Defining a logger for the project
"""
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("logs/provisioning.log"),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )
    return logging.getLogger()


logger = setup_logging()
