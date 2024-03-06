import emoji


def is_category_marker_valid(marker: str) -> bool:
    return emoji.is_emoji(marker)


__all__ = (
    is_category_marker_valid,
)
