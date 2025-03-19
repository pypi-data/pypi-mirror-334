import importlib.metadata


__all__ = [
    "get_version"
]


def get_version() -> str:
    try:
        return importlib.metadata.version("pylibutils")
    except ModuleNotFoundError:
        return "Couldn't get pylibutils version!"


