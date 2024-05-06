import pdfplumber
import logging


logger = logging.getLogger(__name__)


class WrongNumberOfColumns(Exception):
    COLUMN_NUMBER = 9

    def __init__(self, file, ind, current_number):
        super().__init__(f"Number of columns in file {file} is incorrect, \
            shoud be {self.COLUMN_NUMBER} but now is {current_number}, \
            table number is {ind+1}")


class KazFileParser:
    @classmethod
    def read_file(cls, path):
        pdf = pdfplumber.open(path)
        logger.info(f"Found {len(pdf.pages)} tables")
        for page in pdf.pages:
            yield page.extract_tables()
            page.flush_cache()
