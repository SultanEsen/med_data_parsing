import logging

from parsers.uzb import UZBCrawler
from parsers.uzb_pdf import read_file
from utils import get_files


def main():
    crawler = UZBCrawler(UZBCrawler.MAIN_URL)
    file = get_files(UZBCrawler.DOCUMENTS_DIRECTORY)[0]
    read_file(file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
