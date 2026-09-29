import json
from collections import defaultdict


INPUT_FILE = "comparison_results.json"
OUTPUT_FILE = "summary_report.json"


def main():

    # -----------------------------------
    # Load comparison results
    # -----------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    comparisons = data.get(
        "comparisons",
        []
    )

    # -----------------------------------
    # Group results by package
    # -----------------------------------

    packages = defaultdict(list)

    for result in comparisons:

        packages[
            result["package"]
        ].append(result)

    package_summaries = []

    # -----------------------------------
    # Create package summaries
    # -----------------------------------

    for package_name, results in sorted(
        packages.items()
    ):

        version_count = len(results)

        status_counts = {
            "consistent": 0,
            "partial_discrepancy": 0,
            "version_mismatch": 0,
            "not_documented": 0
        }

        dependency_issues = 0
        command_issues = 0

        for result in results:

            status = result.get(
                "overall_status",
                "unknown"
            )

            if status in status_counts:

                status_counts[
                    status
                ] += 1

            dependencies = result.get(
                "discrepancies",
                {}
            ).get(
                "dependencies",
                {}
            )

            commands = result.get(
                "discrepancies",
                {}
            ).get(
                "commands",
                {}
            )

            if (
                dependencies.get(
                    "documented_but_not_used"
                )
                or
                dependencies.get(
                    "used_but_not_documented"
                )
            ):

                dependency_issues += 1

            if (
                commands.get(
                    "documented_but_not_automated"
                )
                or
                commands.get(
                    "automated_but_not_documented"
                )
            ):

                command_issues += 1

        # -----------------------------------
        # Determine package summary
        # -----------------------------------

        if status_counts["consistent"] == version_count:

            package_status = "consistent"

        elif status_counts["version_mismatch"] > 0:

            package_status = "version_mismatch"

        elif status_counts["partial_discrepancy"] > 0:

            package_status = "partial_discrepancy"

        else:

            package_status = "not_documented"

        package_summaries.append({

            "package":
                package_name,

            "script_versions_analyzed":
                version_count,

            "overall_status":
                package_status,

            "status_counts":
                status_counts,

            "versions_with_dependency_issues":
                dependency_issues,

            "versions_with_command_issues":
                command_issues
        })

    # -----------------------------------
    # Global statistics
    # -----------------------------------

    total_versions = len(
        comparisons
    )

    total_consistent = sum(
        1
        for result in comparisons
        if result.get(
            "overall_status"
        ) == "consistent"
    )

    total_partial = sum(
        1
        for result in comparisons
        if result.get(
            "overall_status"
        ) == "partial_discrepancy"
    )

    total_version_mismatch = sum(
        1
        for result in comparisons
        if result.get(
            "overall_status"
        ) == "version_mismatch"
    )

    total_not_documented = sum(
        1
        for result in comparisons
        if result.get(
            "overall_status"
        ) == "not_documented"
    )

    # -----------------------------------
    # Final summary
    # -----------------------------------

    summary = {

        "project":
            "AI-Powered Documentation-Script Consistency Analyzer",

        "total_packages":
            data.get(
                "total_packages",
                0
            ),

        "total_script_versions":
            total_versions,

        "wiki_pages_found":
            data.get(
                "wiki_pages_found",
                0
            ),

        "wiki_pages_missing":
            data.get(
                "wiki_pages_missing",
                0
            ),

        "global_statistics": {

            "consistent":
                total_consistent,

            "partial_discrepancy":
                total_partial,

            "version_mismatch":
                total_version_mismatch,

            "not_documented":
                total_not_documented
        },

        "package_summaries":
            package_summaries
    }

    # -----------------------------------
    # Save
    # -----------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    # -----------------------------------
    # Console output
    # -----------------------------------

    print()

    print(
        "Summary report created:"
    )

    print(
        OUTPUT_FILE
    )

    print()

    print(
        "Packages:",
        data.get(
            "total_packages",
            0
        )
    )

    print(
        "Script versions:",
        total_versions
    )

    print()

    print(
        "GLOBAL STATISTICS"
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


if __name__ == "__main__":

    main()