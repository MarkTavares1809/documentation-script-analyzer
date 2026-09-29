from bs4 import BeautifulSoup
import re
import os


def parse_wiki(wiki_path):

    if not os.path.exists(wiki_path):
        print("Wiki file not found:", wiki_path)
        return {}

    # -----------------------------------
    # Read Wiki HTML
    # -----------------------------------

    with open(
        wiki_path,
        "r",
        encoding="utf-8"
    ) as file:
        html = file.read()

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # -----------------------------------
    # Remove unnecessary HTML
    # -----------------------------------

    for element in soup(
        ["script", "style", "nav"]
    ):
        element.decompose()

    # -----------------------------------
    # Extract visible text
    # -----------------------------------

    text = soup.get_text("\n")

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    text = "\n".join(lines)

    # -----------------------------------
    # 1. Package name
    # -----------------------------------

    package = os.path.basename(
        wiki_path
    )

    package = os.path.splitext(
        package
    )[0]

    # -----------------------------------
    # 2. Find documented build-script
    #    versions
    # -----------------------------------

    versions = []

    # Look specifically at links to build scripts.
    #
    # Example:
    # scripts/master/Alfresco/23.2.1/
    # build_alfresco.sh

    for link in soup.find_all("a"):

        href = link.get("href", "")

        link_text = link.get_text(
            " ",
            strip=True
        )

        combined = (
            href + " " + link_text
        )

        # Only consider links that point
        # to a build .sh script.
        if not re.search(
            r"build_[^/\"'\s]+\.sh",
            combined,
            re.IGNORECASE
        ):
            continue

        # Look for a version immediately
        # before the build script.
        matches = re.findall(
            r"/(\d+\.\d+(?:\.\d+)*)/"
            r"build_[^/\"'\s]+\.sh",
            combined,
            re.IGNORECASE
        )

        for version in matches:

            versions.append(
                version
            )

    # -----------------------------------
    # Fallback:
    # Look for explicit script paths
    # in the raw HTML.
    # -----------------------------------

    if not versions:

        matches = re.findall(
            r"(?:scripts|master)/"
            r"[^/\"'\s]+/"
            r"(\d+\.\d+(?:\.\d+)*)/"
            r"build_[^/\"'\s]+\.sh",
            html,
            re.IGNORECASE
        )

        versions.extend(
            matches
        )

    versions = sorted(
        set(versions)
    )

    # -----------------------------------
    # 3. Find dependencies
    # -----------------------------------

    dependencies = []

    # -----------------------------------
    # 3A. apt-get install commands
    # -----------------------------------

    apt_patterns = re.findall(
        r"apt-get\s+install(?:\s+-y)?\s+([^\n`]+)",
        text,
        re.IGNORECASE
    )

    for package_list in apt_patterns:

        package_list = package_list.replace(
            "\\",
            " "
        )

        package_list = package_list.replace(
            "|",
            " "
        )

        package_list = package_list.replace(
            ";",
            " "
        )

        for package_name in package_list.split():

            package_name = package_name.strip(
                "\"'`()"
            )

            if package_name.startswith("-"):
                continue

            if "$" in package_name:
                continue

            if package_name in [
                "sudo",
                "tee",
                "apt-get"
            ]:
                continue

            if re.match(
                r"^[a-zA-Z0-9][a-zA-Z0-9+._:-]*$",
                package_name
            ):

                dependencies.append(
                    package_name
                )

    # -----------------------------------
    # 3B. Important dependency keywords
    # -----------------------------------

    dependency_keywords = [

        "gcc",
        "g++",

        "clang",
        "clang-tools",

        "cmake",

        "python",
        "python3",

        "java",
        "openjdk",

        "maven",

        "golang",

        "git",

        "curl",
        "wget",

        "make",

        "build-essential",

        "protobuf",

        "netty",

        "zip",
        "unzip"
    ]

    for dependency in dependency_keywords:

        if re.search(
            r"\b" +
            re.escape(dependency) +
            r"\b",
            text,
            re.IGNORECASE
        ):

            dependencies.append(
                dependency
            )

    dependencies = sorted(
        set(dependencies)
    )

    # -----------------------------------
    # 4. Find commands
    # -----------------------------------

    commands = []

    command_patterns = [

        r"sudo\s+apt-get\s+update",

        r"sudo\s+apt-get\s+install\s+[^\n]+",

        r"git\s+clone\s+[^\n]+",

        r"git\s+checkout\s+[^\n]+",

        r"git\s+apply\s+[^\n]+",

        r"wget\s+[^\n]+",

        r"curl\s+[^\n]+",

        r"bash\s+\S+\.sh",

        r"\./\S+\.sh",

        r"\bmake\s+[^\n]+",

        r"\bcmake\s+[^\n]+"
    ]

    for pattern in command_patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for command in matches:

            command = command.strip()

            if command not in commands:

                commands.append(
                    command
                )

    # -----------------------------------
    # 5. Find headings
    # -----------------------------------

    headings = []

    for heading in soup.find_all(
        ["h1", "h2", "h3"]
    ):

        heading_text = heading.get_text(
            " ",
            strip=True
        )

        if heading_text:

            headings.append(
                heading_text
            )

    # -----------------------------------
    # 6. Return structured data
    # -----------------------------------

    return {

        "package": package,

        "source": wiki_path,

        "versions": versions,

        "dependencies": dependencies,

        "commands": commands,

        "headings": headings
    }


# -----------------------------------
# Test
# -----------------------------------

if __name__ == "__main__":

    test_file = (
        "data/wiki/alfresco.html"
    )

    data = parse_wiki(
        test_file
    )

    print("WIKI DATA")
    print()

    print("Package:")
    print(data.get("package"))

    print()

    print("Versions:")
    print(data.get("versions"))

    print()

    print("Dependencies:")
    print(data.get("dependencies"))

    print()

    print("Commands:")
    print(data.get("commands"))