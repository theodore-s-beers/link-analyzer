from lxml import html


def get_urls_from_string(page_content: str, base_url: str) -> list[str]:
    tree = html.fromstring(page_content)
    tree.make_links_absolute(base_url)

    links_list: list[str] = []

    for elem in tree.iter():
        if elem.tag == "a":
            links_list.append(elem.get("href"))

    return links_list
