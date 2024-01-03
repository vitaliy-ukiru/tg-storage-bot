from typing import Optional


def optional_str_factory(v) -> Optional[str]:
    if v is None:
        return None

    return str(v)
