from pathlib import Path


def make_title_path(path: str) -> str:
    path = str(path)
    if len(path) > 60:
        parts = Path(path).parts
        parts_count = len(parts)
        if parts_count > 4:
            offset = 4
        elif parts_count > 3:
            offset = 3
        else:
            offset = 2

        path = ".../" + "/".join(parts[-offset:])

    return path
