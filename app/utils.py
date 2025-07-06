# utils.py
import logging
import sys

# basic setup: INFO lines go to the terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def log(msg: str):
    """Simple wrapper so you type log('hello') instead of logging.info(...)"""
    logging.info(msg)

# TODO: try log("Loaded CSV with 500 rows") inside preprocess.py and
# watch it appear in Streamlit’s terminal as you upload files.