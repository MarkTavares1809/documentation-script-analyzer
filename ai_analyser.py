import json
import requests
import time


INPUT_FILE = "comparison_results.json"
OUTPUT_FILE = "ai_analysis.json"

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3.2:latest"


# -----------------------------------
# Ask Ollama
# -----------------------------------

def ask_ai(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        ""
    ).strip()


# -----------------------------------
# Build AI prompt
# -----------------------------------

def build_prompt(result):

    package = result.get(
        "package",
        ""
    )

    version = result.get(
        "version",
        ""
    )

    script = result.get(
        "script",
        ""
    )

    status = result.get(
        "overall_status",
        ""
    )

    version_comparison = result.get(
        "version_comparison",
        {}
    )

    discrepancies = result.get(
        "discrepancies",
        {}
    )

    dependencies = discrepancies.get(
        "dependencies",
        {}
    )

    commands = discrepancies.get(
        "commands",
        {}
    )

    automation = result.get(
        "automation_details",
        {}
    )

    prompt = f"""
You are analyzing documentation versus an automated
Linux on IBM Z build script.

Package: {package}
Script version: {version}
Script: {script}
Overall status: {status}

Documented versions:
{version_comparison.get("documented_versions", [])}

Script version:
{version_comparison.get("script_version", version)}

DEPENDENCY DIFFERENCES

Documented but not used:
{dependencies.get("documented_but_not_used", [])}

Used but not documented:
{dependencies.get("used_but_not_documented", [])}

COMMAND DIFFERENCES

Documented but not automated:
{commands.get("documented_but_not_automated", [])}

Automated but not documented:
{commands.get("automated_but_not_documented", [])}

AUTOMATION DETAILS

Environment variables:
{automation.get("environment_variables", [])}

Sudo commands:
{automation.get("sudo_commands", [])}

Build commands:
{automation.get("build_commands", [])}

TASK:

Explain the comparison using ONLY the supplied evidence.

Keep the explanation concise.

State:
1. What the documentation says.
2. What the script does.
3. What difference was detected.
4. Whether it is a documented discrepancy or simply information
   that is not covered by the documentation.

Do not invent missing information.
Do not assume that an old script version is an error.
Do not call a difference an error unless the supplied evidence
supports that conclusion.

Return only one concise paragraph.
"""

    return prompt


# -----------------------------------
# Main
# -----------------------------------

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

    total = len(comparisons)

    print()
    print(
        "AI ANALYSIS"
    )

    print(
        "Total comparisons:",
        total
    )

    print()

    # -----------------------------------
    # Analyze every comparison
    # -----------------------------------

    ai_results = []

    for index, result in enumerate(
        comparisons,
        start=1
    ):

        print(
            f"Analyzing {index}/{total}..."
        )

        prompt = build_prompt(
            result
        )

        try:

            explanation = ask_ai(
                prompt
            )

        except Exception as error:

            explanation = (
                "AI analysis failed: "
                + str(error)
            )

        ai_results.append({

            "package":
                result.get(
                    "package",
                    ""
                ),

            "version":
                result.get(
                    "version",
                    ""
                ),

            "script":
                result.get(
                    "script",
                    ""
                ),

            "overall_status":
                result.get(
                    "overall_status",
                    ""
                ),

            "ai_explanation":
                explanation
        })

        # Small delay so Ollama isn't
        # overwhelmed by rapid requests.
        time.sleep(0.05)

    # -----------------------------------
    # Final AI output
    # -----------------------------------

    output = {

        "project":
            "AI-Powered Documentation-Script Consistency Analyzer",

        "model":
            MODEL,

        "total_analyzed":
            len(ai_results),

        "results":
            ai_results
    }

    # -----------------------------------
    # Save JSON
    # -----------------------------------

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

    # -----------------------------------
    # Finished
    # -----------------------------------

    print()

    print(
        "================================"
    )

    print(
        "AI ANALYSIS COMPLETED"
    )

    print(
        "================================"
    )

    print(
        "Total analyzed:",
        len(ai_results)
    )

    print(
        "Saved to:",
        OUTPUT_FILE
    )


if __name__ == "__main__":

    main()