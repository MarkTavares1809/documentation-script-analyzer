import json
import os
import re

from script_parser import parse_script


SCRIPTS_PATH = "scripts"
OUTPUT_FILE = "package_inventory.json"


def is_version_folder(name):

    return bool(
        re.fullmatch(
            r"v?\d+(?:\.\d+)+",
            name
        )
    )


def build_inventory():

    inventory = []

    # Go through packages
    for package in sorted(
        os.listdir(SCRIPTS_PATH)
    ):

        # Ignore hidden folders such as .git
        if package.startswith("."):
            continue

        package_path = os.path.join(
            SCRIPTS_PATH,
            package
        )

        if not os.path.isdir(
            package_path
        ):
            continue

        package_data = {
            "package": package,
            "versions": []
        }

        # Go through versions
        for version in sorted(
            os.listdir(package_path)
        ):

            # Only accept actual version folders
            if not is_version_folder(
                version
            ):
                continue

            version_path = os.path.join(
                package_path,
                version
            )

            if not os.path.isdir(
                version_path
            ):
                continue

            version_data = {
                "version": version,
                "scripts": []
            }

            # Find shell scripts
            for filename in sorted(
                os.listdir(version_path)
            ):

                if not filename.endswith(".sh"):
                    continue

                script_path = os.path.join(
                    version_path,
                    filename
                )

                script_data = parse_script(
                    script_path
                )

                version_data["scripts"].append({
                    "file": filename,
                    "data": script_data
                })

            # Only add versions that contain scripts
            if version_data["scripts"]:

                package_data["versions"].append(
                    version_data
                )

        # Only add packages that contain versions
        if package_data["versions"]:

            inventory.append(
                package_data
            )

    return inventory


if __name__ == "__main__":

    inventory = build_inventory()

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            inventory,
            file,
            indent=4
        )

    print(
        f"Package inventory created: {OUTPUT_FILE}"
    )

    print(
        f"Packages found: {len(inventory)}"
    )