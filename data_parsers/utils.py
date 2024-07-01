from pathlib import Path
from pprint import pprint
import asyncio
import logging


logger = logging.getLogger(__name__)


IGNORE_FILES = (".DS_Store", "desktop.ini", "Thumbs.db", ".~lock.", ".csv")


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def check_and_remove_space(value, index):
    if len(value) > index:
        if value[index] == " ":
            value = value[:index] + value[index + 1:]
    return value

def get_latest_files(directory: str):
    def get_creation_time(item):
        return item.stat().st_ctime

    file_path = Path(__file__).parent / "documents" / directory
    items = file_path.iterdir()
    sorted_items = sorted(items, key=get_creation_time, reverse=True)
    files = []
    for file in sorted_items:
        if not any(file.name.endswith(ignore) for ignore in IGNORE_FILES):
            files.append(file)
    return files[0].name


async def wait_for_download(file_location: Path, file_name: str, timeout: int):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < timeout:
            await asyncio.sleep(1)
            download_dir = Path(__file__).parent / Path(file_location)
            logger.info(f"Checking for {download_dir}")
            logger.info(f"Seconds: {seconds}")
            for f in download_dir.iterdir():
                logger.info(f"File: {f.name}, File name: {file_name}, equal: {f.name == file_name}")
                if f.name == file_name:
                    dl_wait = True
                    break
                else:
                    dl_wait = False
                seconds += 1

        return dl_wait