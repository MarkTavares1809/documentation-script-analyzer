import json
import os

from wiki_parser import parse_wiki
from dependency_normalizer import normalize_dependencies
from command_normalizer import normalize_commands


# ============================================================
# CHANGE ONLY THIS LINE
# ============================================================
# Example:
# PACKAGE_TO_CHECK = "bazel"
# PACKAGE_TO_CHECK = "alfresco"
#
# Use None to analyze ALL packages.
PACKAGE_TO_CHECK = "bazel"


INVENTORY_FILE = "package_inventory.json"
WIKI_DIR = "data/wiki"
OUTPUT_FILE = "comparison_results.json"


def compare_version(script_version, documented_versions):
    if not documented_versions:
        return {
            "status": "not_documented",
            "script_version": script_version,
            "documented_versions": []
        }

    if script_version in documented_versions:
        status = "match"
    else:
        status = "mismatch"

    return {
        "status": status,
        "script_version": script_version,
        "documented_versions": documented_versions
    }


def compare_dependencies(script_dependencies, wiki_dependencies):
    script_dependencies = set(
        normalize_dependencies(script_dependencies)
    )

    wiki_dependencies = set(
        normalize_dependencies(wiki_dependencies)
    )

    documented_but_not_used = sorted(
        wiki_dependencies - script_dependencies
    )

    used_but_not_documented = sorted(
        script_dependencies - wiki_dependencies
    )

    return {
        "documented_but_not_used": documented_but_not_used,
        "used_but_not_documented": used_but_not_documented
    }


def compare_commands(script_commands, wiki_commands):
    script_commands = set(
        normalize_commands(script_commands)
    )

    wiki_commands = set(
        normalize_commands(wiki_commands)
    )

    documented_but_not_automated = sorted(
        wiki_commands - script_commands
    )

    automated_but_not_documented = sorted(
        script_commands - wiki_commands
    )

    return {
        "documented_but_not_automated": documented_but_not_automated,
        "automated_but_not_documented": automated_but_not_documented
    }


def determine_status(
    version_comparison,
    dependency_comparison,
    command_comparison
):

    if version_comparison["status"] == "not_documented":
        return "not_documented"

    if version_comparison["status"] == "mismatch":
        return "version_mismatch"

    dependency_issue = (
        dependency_comparison["documented_but_not_used"]
        or
        dependency_comparison["used_but_not_documented"]
    )

    command_issue = (
        command_comparison["documented_but_not_automated"]
        or
        command_comparison["automated_but_not_documented"]
    )

    if not dependency_issue and not command_issue:
        return "consistent"

    return "partial_discrepancy"


def compare_package(package_data):

    package = package_data["package"]

    wiki_file = os.path.join(
        WIKI_DIR,
        package.lower() + ".html"
    )

    wiki_data = parse_wiki(wiki_file)

    documented_versions = wiki_data.get(
        "versions",
        []
    )

    results = []

    for version_data in package_data["versions"]:

        version = version_data["version"]

        for script_data in version_data["scripts"]:

            script = script_data["file"]
            script_info = script_data["data"]

            version_comparison = compare_version(
                version,
                documented_versions
            )

            dependency_comparison = compare_dependencies(
                script_info.get("dependencies", []),
                wiki_data.get("dependencies", [])
            )

            command_comparison = compare_commands(
                script_info.get("build_commands", []),
                wiki_data.get("commands", [])
            )

            overall_status = determine_status(
                version_comparison,
                dependency_comparison,
                command_comparison
            )

            result = {
                "package": package,
                "version": version,
                "script": script,
                "wiki_source": wiki_file,

                "overall_status": overall_status,

                "version_comparison": version_comparison,

                "discrepancies": {
                    "dependencies": dependency_comparison,
                    "commands": command_comparison
                },

                "automation_details": {
                    "environment_variables": script_info.get(
                        "environment_variables",
                        []
                    ),
                    "sudo_commands": script_info.get(
                        "sudo_commands",
                        []
                    ),
                    "build_commands": script_info.get(
                        "build_commands",
                        []
                    )
                }
            }

            results.append(result)

    return results


def main():

    print("======================================")
    print("DOCUMENTATION-SCRIPT COMPARATOR")
    print("======================================")

    if PACKAGE_TO_CHECK:
        print("Package selected:", PACKAGE_TO_CHECK)
    else:
        print("Package selected: ALL")

    print()

    with open(
        INVENTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        inventory = json.load(file)

    # --------------------------------------------------------
    # Select package
    # --------------------------------------------------------

    if PACKAGE_TO_CHECK:

        selected_packages = [
            package
            for package in inventory
            if package["package"].lower()
            == PACKAGE_TO_CHECK.lower()
        ]

        if not selected_packages:

            print(
                "ERROR: Package not found:",
                PACKAGE_TO_CHECK
            )

            print()
            print("Available packages:")

            for package in inventory:
                print("-", package["package"])

            return

    else:

        selected_packages = inventory

    # --------------------------------------------------------
    # Compare selected packages
    # --------------------------------------------------------

    comparisons = []

    for package_data in selected_packages:

        print(
            "Analyzing:",
            package_data["package"]
        )

        results = compare_package(
            package_data
        )

        comparisons.extend(results)

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_consistent = sum(
        1
        for result in comparisons
        if result["overall_status"]
        == "consistent"
    )

    total_partial = sum(
        1
        for result in comparisons
        if result["overall_status"]
        == "partial_discrepancy"
    )

    total_version_mismatch = sum(
        1
        for result in comparisons
        if result["overall_status"]
        == "version_mismatch"
    )

    total_not_documented = sum(
        1
        for result in comparisons
        if result["overall_status"]
        == "not_documented"
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    output = {
        "project":
            "AI-Powered Documentation-Script Consistency Analyzer",

        "selected_package":
            PACKAGE_TO_CHECK,

        "total_packages":
            len(selected_packages),

        "wiki_pages_found":
            sum(
                1
                for package in selected_packages
                if os.path.exists(
                    os.path.join(
                        WIKI_DIR,
                        package["package"].lower() + ".html"
                    )
                )
            ),

        "wiki_pages_missing":
            sum(
                1
                for package in selected_packages
                if not os.path.exists(
                    os.path.join(
                        WIKI_DIR,
                        package["package"].lower() + ".html"
                    )
                )
            ),

        "total_script_versions":
            len(comparisons),

        "status_statistics": {
            "consistent":
                total_consistent,

            "partial_discrepancy":
                total_partial,

            "version_mismatch":
                total_version_mismatch,

            "not_documented":
                total_not_documented
        },

        "comparisons":
            comparisons
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("======================================")
    print("COMPARISON COMPLETED")
    print("======================================")

    print(
        "Packages analyzed:",
        len(selected_packages)
    )

    print(
        "Script versions compared:",
        len(comparisons)
    )

    print(
        "Consistent:",
        total_consistent
    )

    print(
        "Partial discrepancies:",
        total_partial
    )

    print(
        "Version mismatches:",
        total_version_mismatch
    )

    print(
        "Not documented:",
        total_not_documented
    )

    print()
    print(
        "Results saved to:",
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()