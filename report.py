from typing import Optional


def report_links(pages: dict[str, Optional[int]]) -> str:
    actual_pages = remove_none_values(pages)
    pages_list = sort_pages(actual_pages)

    report = ""

    for page in pages_list:
        if page[1] > 1:
            report += f"Found {page[1]} internal links to {page[0]}\n"
        else:
            report += f"Found 1 internal link to {page[0]}\n"

    return report.strip()


def report_errors(errors: str) -> str:
    stripped = errors.strip()

    if stripped != "":
        intro = "\nThe following errors were encountered:\n"
        return intro + stripped

    return ""


def remove_none_values(pages: dict[str, Optional[int]]) -> dict[str, int]:
    return {k: v for k, v in pages.items() if v is not None}


def sort_pages(pages: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(pages.items(), key=lambda x: x[1], reverse=True)
