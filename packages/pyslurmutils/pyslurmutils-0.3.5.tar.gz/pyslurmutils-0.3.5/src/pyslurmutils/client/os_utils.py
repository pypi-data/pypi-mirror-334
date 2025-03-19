import os


def chmod(path) -> None:
    try:
        original_umask = os.umask(0)
        return os.chmod(path, mode=0o777)
    finally:
        os.umask(original_umask)


def makedirs(dirname: str) -> None:
    try:
        original_umask = os.umask(0)
        return os.makedirs(dirname, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)
