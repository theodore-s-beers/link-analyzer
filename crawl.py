from typing import Optional
from urllib.parse import urlparse

from lxml import html
from requests import get, Response


def crawl_page(
    base_url: str,
    current_url: str = "",
    pages: dict[str, Optional[int]] = {},
    errors: str = "",
) -> tuple[dict[str, Optional[int]], str]:
    if current_url == "":
        current_url = base_url

    current_normalized = normalize_url(current_url)

    if current_normalized not in pages:
        pages[current_normalized] = 0

    parsed_base = urlparse(base_url)
    parsed_current = urlparse(current_url)

    if parsed_base.netloc != parsed_current.netloc:
        pages[current_normalized] = None

    if pages[current_normalized] is None:
        return (pages, errors)

    if pages[current_normalized] > 0:
        pages[current_normalized] += 1
        return (pages, errors)

    # In case of a bad URL...
    try:
        current_page = get(current_url)
    except Exception:
        errors += f"Could not complete GET request to {current_url}\n"
        pages[current_normalized] = None
        return (pages, errors)

    try:
        validate_response(current_page, current_url)

        pages[current_normalized] += 1

        urls = get_urls_from_string(current_page.text, current_url)

        for url in urls:
            results = crawl_page(base_url, url, pages, errors)
            pages = results[0]
            errors = results[1]

        return (pages, errors)
    except Exception as e:
        errors += f"{e}\n"
        pages[current_normalized] = None
        return (pages, errors)


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    domain_and_path = parsed_url.netloc + parsed_url.path
    truncated = domain_and_path.strip("/")
    return truncated.lower()


def validate_response(resp: Response, url: str) -> None:
    if resp.status_code != 200:
        raise Exception(f"Bad status code, {resp.status_code}, for {url}")

    if "text/html" not in resp.headers["Content-Type"]:
        raise Exception(f"Bad content type, {resp.headers['Content-Type']}, for {url}")


def get_urls_from_string(page_content: str, base_url: str) -> list[str]:
    tree = html.fromstring(page_content)
    tree.make_links_absolute(base_url)

    links_list: list[str] = []

    for elem in tree.iter():
        if elem.tag == "a":
            links_list.append(elem.get("href"))

    return links_list
