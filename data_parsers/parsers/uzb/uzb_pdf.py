# import tabula
import pdfplumber
import logging


logger = logging.getLogger(__name__)


class UZBFileParser:
    @classmethod
    def read_file(cls, path):
        logger.info(f"Reading file {path}")
        pdf = pdfplumber.open(path)
        # tables = [page.extract_table() for page in pdf.pages]
        logger.info(f"Found {len(pdf.pages)} tables")
        for page in pdf.pages:
            yield page.extract_tables()
            page.flush_cache()
