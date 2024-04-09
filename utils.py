from pathlib import Path


def get_files(directory):
    file_path = Path(__file__).parent / "documents" / directory
    return list(file_path.iterdir())
