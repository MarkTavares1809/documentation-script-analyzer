AI-Powered Documentation–Script Consistency Analyzer
1. Project Overview
The AI-Powered Documentation–Script Consistency Analyzer is a Python-based tool that compares Linux on IBM Z build documentation with automated build scripts.

The system analyzes whether documented build instructions are consistent with the commands, dependencies, and build procedures implemented in automation scripts.

The project uses deterministic parsing and comparison techniques to identify differences and uses a local Large Language Model (LLM) through Ollama to generate concise explanations of detected differences.

2. Problem Statement
Linux on IBM Z contains documentation describing how different software packages can be built and installed.

At the same time, automated build scripts are maintained separately.

Over time, documentation and automation can become inconsistent.

Manually comparing hundreds of packages and script versions is time-consuming.

This project automates the comparison process and generates structured reports showing potential discrepancies.

3. Objectives
The main objectives are:

Collect Linux on IBM Z build scripts.
Collect corresponding build documentation from the GitHub Wiki.
Extract package versions from automated scripts.
Extract dependencies and build commands.
Extract dependencies and commands from documentation.
Normalize differences in package and command naming.
Compare documentation with automation.
Identify discrepancies.
Generate structured JSON reports.
Use a local LLM to explain detected differences.

4. Data Sources
Documentation

Linux on IBM Z documentation:

https://github.com/linux-on-ibm-z/docs/wiki/

Automated Scripts

Linux on IBM Z scripts:

https://github.com/linux-on-ibm-z/scripts

5. System Architecture
The system follows this workflow:

Linux on IBM Z Wiki
        |
        v
  github_fetcher.py
        |
        v
    data/wiki/
        |
        v
   wiki_parser.py
        |
        |
        +-------------------+
                            |
                            v
                       comparator.py
                            ^
                            |
        +-------------------+
        |
 Linux on IBM Z Scripts
        |
        v
   script_parser.py
        |
        v
Dependency / Command
   Normalization
        |
        v
Comparison Results
        |
        +----------------------+
        |                      |
        v                      v
summary_report.py       ai_analyzer.py
        |                      |
        v                      v
summary_report.json     ai_analysis.json

6. Project Structure
documentation-script-analyzer/
│
├── scripts/
│   └── Linux on IBM Z build scripts
│
├── main.py
├── github_fetcher.py
├── script_parser.py
├── wiki_parser.py
├── dependency_normalizer.py
├── command_normalizer.py
├── comparator.py
├── summary_report.py
├── ai_analyzer.py
│
├── comparison_results.json
├── summary_report.json
├── ai_analysis.json
│
├── requirements.txt
└── README.md
Generated Files

The following files/directories are generated automatically during execution and therefore do not need to be included in the GitHub repository:

data/wiki/
package_inventory.json

github_fetcher.py automatically creates the data/wiki/ directory and downloads the required Wiki pages.

main.py automatically generates package_inventory.json.

7. Main Components
main.py

Scans the cloned scripts repository and creates an inventory of available packages, versions, and shell scripts.

Output:

package_inventory.json

This file is generated automatically and does not need to be uploaded to GitHub.

github_fetcher.py

Downloads the corresponding Linux on IBM Z Wiki pages.

The downloaded pages are stored in:

data/wiki/

The data/wiki/ directory is generated automatically when this script is executed.

script_parser.py

Analyzes shell scripts and extracts:

Dependencies
Sudo commands
Build commands
Environment variables
Script versions
wiki_parser.py

Analyzes documentation pages and extracts:

Documented versions
Dependencies
Build commands
Documentation headings
dependency_normalizer.py

Normalizes dependency names so that equivalent packages can be compared.

For example:

gcc-12
gcc-13

can be normalized to:

gcc

This reduces false differences caused by version-specific package names.

command_normalizer.py

Normalizes build commands before comparison.

For example:

sudo ./build.sh

and:

./build.sh

can be normalized into a comparable representation.

comparator.py

Compares the parsed documentation and automation data.

It checks:

Version differences
Dependency differences
Command differences

Possible statuses include:

consistent
partial_discrepancy
version_mismatch
not_documented
summary_report.py

Aggregates comparison results at package level and generates:

summary_report.json
ai_analyzer.py

Uses a locally running Ollama model to explain comparison results.

The current model is:

llama3.2:latest

The AI receives structured comparison evidence and produces a concise explanation.

The AI is instructed not to invent information that is not present in the comparison data.

8. Installation
Step 1: Install Python

Python 3.x is required.

Verify the installation:

python --version
Step 2: Install Python Dependencies

From the project directory, run:

pip install -r requirements.txt
Step 3: Clone the Linux on IBM Z Scripts Repository

The analyzer expects the scripts repository to be located inside the project directory as scripts.

From inside the project directory, run:

git clone https://github.com/linux-on-ibm-z/scripts.git scripts

The resulting structure should be:

documentation-script-analyzer/
└── scripts/
    ├── Alfresco/
    ├── AntLR/
    ├── ApacheCassandra/
    ├── ApacheHttpServer/
    └── ...
Step 4: Install Ollama

Install Ollama and make sure it is running.

Verify the available models:

ollama list

The project currently uses:

llama3.2:latest

If the model is not installed:

ollama pull llama3.2

9. Running the Project
Run the following steps in this order.

Step 1: Download Wiki Documentation

Run:

python github_fetcher.py

This downloads the corresponding Wiki pages and creates:

data/wiki/

The Wiki files are generated automatically and do not need to be included in the GitHub repository.

Step 2: Build the Package Inventory

Run:

python main.py

This scans the scripts/ directory and generates:

package_inventory.json

This file is also generated automatically.

Step 3: Compare Documentation and Scripts

Run:

python comparator.py

This generates:

comparison_results.json
Step 4: Generate the Summary Report

Run:

python summary_report.py

This generates:

summary_report.json
Step 5: Run AI Analysis

Make sure Ollama is running.

Then execute:

python ai_analyzer.py

This generates:

ai_analysis.json

10. Output Files
package_inventory.json

Contains the discovered packages, versions, and scripts.

Generated automatically by main.py.

comparison_results.json

Contains detailed comparisons between documentation and automation.

summary_report.json

Contains package-level and global statistics.

ai_analysis.json

Contains AI-generated explanations for each comparison.

11. Comparison Logic
The analyzer checks three main areas.

Version Comparison

Checks whether the script version appears in the documented versions.

Dependency Comparison

Checks for:

Documented but not used
Used but not documented
Command Comparison

Checks for:

Documented but not automated
Automated but not documented

12. AI Analysis
The project uses a local LLM instead of sending project data to an external AI service.
The AI receives structured evidence such as:

Package name
Script version
Documentation versions
Dependency differences
Command differences
Build commands
Environment variables

The model then produces a concise explanation.

The AI layer is used for interpretation and explanation rather than replacing the deterministic comparison logic.

13. Current Analysis
The current dataset contains:

80 packages
80 Wiki pages
1,618 script versions analyzed

The comparison generated the following statuses:

Consistent:              0
Partial discrepancies:   47
Version mismatches:      1062
Not documented:          509

These results are based on the repository contents and parser rules used during the current project analysis.

A version mismatch does not automatically mean that the documentation is incorrect. Historical script versions may exist even when the Wiki documents a different current version.

Note: These statistics represent the dataset and analysis performed during project testing. Results may change if the source repositories or Wiki documentation are updated.

14. Limitations
The current implementation uses heuristic parsing.
Potential limitations include:

Shell scripts can contain complex shell syntax.
Documentation formatting may change.
Package names can vary between distributions.
Equivalent commands may be written in different ways.
Historical script versions may not be represented in current documentation.
Version mismatch does not necessarily indicate an actual documentation error.
The AI explanation is limited to the evidence supplied by the comparison engine.
Wiki pages must be successfully downloaded before comparison.

15. Future Improvements
Possible future improvements include:

More advanced shell-script parsing.
Better semantic command comparison.
More accurate version matching.
Automatic detection of current versus historical versions.
HTML report generation.
Web-based dashboard.
Confidence scores for detected discrepancies.
Automatic issue generation for confirmed documentation problems.
Support for additional Linux distributions.
More advanced local LLM models.

16. Technologies Used
Python
GitHub
BeautifulSoup
Requests
Regular Expressions
JSON
Ollama
Llama 3.2


17. Conclusion
The project provides an automated approach for analyzing consistency between Linux on IBM Z build documentation and automated build scripts.
It combines deterministic parsing, normalization, comparison, reporting, and local LLM-based explanation to reduce the manual effort required to identify and understand potential documentation inconsistencies.