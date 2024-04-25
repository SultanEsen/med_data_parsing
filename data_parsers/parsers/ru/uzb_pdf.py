import tabula
import logging


class UZBFileParser:
    @classmethod
    def read_file(cls, path):
        logging.info(f"Reading file {path}")
        tables = tabula.read_pdf(path, pages="all")
        # logging.info(f"Found {len(tables)} tables")
        return tables
