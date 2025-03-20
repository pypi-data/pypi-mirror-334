import os


def safe_path(path: str, allowed_roots: list[str]) -> str:
    if os.path.isdir(path):
        real_path = os.path.realpath(path)
        if not any((real_path + os.sep).startswith(root + os.sep) for root in allowed_roots):
            raise ValueError("illegal path access")
        return real_path
    else:
        real_path = os.path.realpath(path)
        if not any(real_path.startswith(root + os.sep) for root in allowed_roots):
            raise ValueError("illegal path access")
        return real_path


def safe_join(base: str, *paths: str) -> str:
    real_base = os.path.realpath(base)
    real_path = os.path.realpath(os.path.join(base, *paths))

    if real_path.startswith(real_base + os.sep):
        return real_path
    else:
        raise ValueError("illegal path access")
