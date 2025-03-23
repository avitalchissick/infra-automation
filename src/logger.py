"""
Defining a logger for the project
"""
import logging
import os


def setup_logging():
    if not os.path.exists("logs"):
        os.mkdir("logs")

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
