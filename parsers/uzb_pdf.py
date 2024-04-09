import camelot
import logging


def read_file(path):
    tables = camelot.read_pdf(path, pages="all")
    logging.info(f"Found {len(tables)} tables")
