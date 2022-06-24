from typing import Optional


def remove_none_values(dict: dict[str, Optional[str]]) -> dict[str, str]:
    return {k: v for k, v in dict.items() if v is not None}


def sort_pages(dict: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)
