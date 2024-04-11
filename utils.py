from pathlib import Path


def get_latest_files(directory):
    def get_creation_time(item):
        return item.stat().st_ctime

    file_path = Path(__file__).parent / "documents" / directory
    items = file_path.iterdir()
    sorted_items = sorted(items, key=get_creation_time, reverse=True)
    return sorted_items[0].name
