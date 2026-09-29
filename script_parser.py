import re
import os


def parse_script(script_path):

    if not os.path.exists(script_path):
        print("Script not found:", script_path)
        return {}

    with open(
        script_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        content = file.read()

    # -----------------------------------
    # Dependencies
    # -----------------------------------

    dependencies = []

    lines = content.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if "apt-get install" in line:

            command = line

            # Collect continuation lines
            while command.endswith("\\"):

                command = command[:-1].strip()

                i += 1

                if i >= len(lines):
                    break

                command += " " + lines[i].strip()

            # Get everything after apt-get install
            if "apt-get install" in command:

                packages_text = command.split(
                    "apt-get install",
                    1
                )[1]

                # Remove common apt options
                packages_text = re.sub(
                    r"--[a-zA-Z0-9_-]+(?:=[^\s]+)?",
                    " ",
                    packages_text
                )

                packages_text = re.sub(
                    r"(?<!\w)-y(?!\w)",
                    " ",
                    packages_text
                )

                # Remove shell syntax
                packages_text = packages_text.replace(
                    "|", " "
                )

                packages_text = packages_text.replace(
                    ";", " "
                )

                # Extract possible package names
                for package in packages_text.split():

                    package = package.strip(
                        "\"'`"
                    )

                    # Ignore shell variables
                    if "$" in package:
                        continue

                    # Ignore shell characters
                    if package in [
                        "\\",
                        "tee",
                        "sudo"
                    ]:
                        continue

                    if package.startswith("-"):
                        continue

                    # Only keep package-like names
                    if re.match(
                        r"^[a-zA-Z0-9][a-zA-Z0-9+._:-]*$",
                        package
                    ):
                        dependencies.append(
                            package
                        )

        i += 1

    # -----------------------------------
    # SUDO commands
    # -----------------------------------

    sudo_commands = re.findall(
        r"^\s*sudo\s+.*",
        content,
        re.MULTILINE
    )

    # -----------------------------------
    # Environment variables
    # -----------------------------------

    variables = re.findall(
        r"\$\{?([A-Z][A-Z0-9_]*)\}?",
        content
    )

    # -----------------------------------
    # Build commands
    # -----------------------------------

    build_commands = []

    for line in content.splitlines():

        line = line.strip()

        if (
            line.startswith("./")
            or line.startswith("make ")
            or line.startswith("cmake ")
            or line.startswith("bash ")
        ):
            build_commands.append(line)

    return {
        "script_path": script_path,
        "dependencies": sorted(
            set(dependencies)
        ),
        "sudo_commands": sorted(
            set(sudo_commands)
        ),
        "build_commands": sorted(
            set(build_commands)
        ),
        "environment_variables": sorted(
            set(variables)
        )
    }


if __name__ == "__main__":

    test_script = (
        "scripts/Bazel/9.2.0/"
        "build_bazel.sh"
    )

    data = parse_script(
        test_script
    )

    print("SCRIPT DATA")

    print(data)