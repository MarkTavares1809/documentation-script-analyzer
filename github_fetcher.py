import requests
import os
import re


WIKI_BASE_URL = "https://github.com/linux-on-ibm-z/docs/wiki/"

SCRIPTS_DIR = "scripts"
WIKI_DIR = "data/wiki"


def package_to_wiki_name(package):

    # Convert common repository naming styles
    name = package.replace("_", "-")

    return name


def fetch_wiki_page(package):

    wiki_name = package_to_wiki_name(package)

    url = WIKI_BASE_URL + "Building-" + wiki_name

    response = requests.get(url)

    if response.status_code != 200:
        return None

    # GitHub may return a page even when the Wiki page
    # does not exist, so check for the actual page title.
    if "Page not found" in response.text:
        return None

    os.makedirs(WIKI_DIR, exist_ok=True)

    file_name = package.lower() + ".html"

    file_path = os.path.join(
        WIKI_DIR,
        file_name
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(response.text)

    return file_path


def main():

    os.makedirs(WIKI_DIR, exist_ok=True)

    packages = []

    for item in os.listdir(SCRIPTS_DIR):

        item_path = os.path.join(
            SCRIPTS_DIR,
            item
        )

        if (
            os.path.isdir(item_path)
            and not item.startswith(".")
        ):
            packages.append(item)

    packages = sorted(packages)

    print("Packages found:", len(packages))

    successful = []
    failed = []

    # Start with first 5 packages
    test_packages = packages

    print("\n Downloading Wiki pages for all packages:")
    
    for package in test_packages:

        print("\nChecking:", package)

        path = fetch_wiki_page(package)

        if path:

            print("SUCCESS:", path)
            successful.append(package)

        else:

            print("FAILED:", package)
            failed.append(package)

    print("\n==============================")
    print("SUCCESSFUL:", len(successful))
    print("FAILED:", len(failed))
    print("==============================")


if __name__ == "__main__":
    main()