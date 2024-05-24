from pathlib import Path
from pprint import pprint


IGNORE_FILES = (".DS_Store", "desktop.ini", "Thumbs.db", ".~lock.")


def get_latest_files(directory: str):
    def get_creation_time(item):
        return item.stat().st_ctime

    file_path = Path(__file__).parent / "documents" / directory
    items = file_path.iterdir()
    sorted_items = sorted(items, key=get_creation_time, reverse=True)
    files = []
    for file in sorted_items:
        if not any(file.name.startswith(ignore) for ignore in IGNORE_FILES):
            files.append(file)
    return files[0].name
