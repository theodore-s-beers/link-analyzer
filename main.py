import sys

from crawl import crawl_page
from report import report_errors, report_links


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <base_url>")
        sys.exit(1)

    base_url = sys.argv[1]

    results = crawl_page(base_url)
    links = results[0]
    errors = results[1]

    links_report = report_links(links)
    print(links_report)

    error_report = report_errors(errors)
    if error_report != "":
        print(error_report)


if __name__ == "__main__":
    main()
