from pathlib import Path


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def find_single_file(directory: str, extension: str):
    files = list(Path(directory).glob(f"*{extension}"))
    if not files:
        raise FileNotFoundError(f"No {extension} file found in {directory}")
    return files[0]
