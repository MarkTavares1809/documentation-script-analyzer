import re


def normalize_command(command):

    command = command.strip().lower()

    # -----------------------------------
    # Remove sudo
    # -----------------------------------

    command = re.sub(
        r"^sudo\s+",
        "",
        command
    )

    # -----------------------------------
    # Normalize bash/sh script execution
    # -----------------------------------

    command = re.sub(
        r"^(bash|sh)\s+",
        "",
        command
    )

    command = re.sub(
        r"^\./",
        "",
        command
    )

    # -----------------------------------
    # Remove extra spaces
    # -----------------------------------

    command = re.sub(
        r"\s+",
        " ",
        command
    ).strip()

    # -----------------------------------
    # Normalize apt-get install
    # -----------------------------------

    command = re.sub(
        r"apt-get\s+install\s+-y",
        "apt-get install",
        command
    )

    command = re.sub(
        r"apt\s+install\s+-y",
        "apt install",
        command
    )

    # -----------------------------------
    # Normalize curl options
    # -----------------------------------

    command = re.sub(
        r"curl\s+-[a-zA-Z]+",
        "curl",
        command
    )

    # -----------------------------------
    # Normalize wget options
    # -----------------------------------

    command = re.sub(
        r"wget\s+-[a-zA-Z]+",
        "wget",
        command
    )

    # -----------------------------------
    # Remove trailing shell characters
    # -----------------------------------

    command = command.rstrip(
        "\\;"
    ).strip()

    return command


def normalize_commands(commands):

    normalized = []

    for command in commands:

        normalized_command = normalize_command(
            command
        )

        if normalized_command:

            normalized.append(
                normalized_command
            )

    return sorted(
        set(normalized)
    )


# -----------------------------------
# Test
# -----------------------------------

if __name__ == "__main__":

    test_commands = [

        "bash build_alfresco.sh",

        "./build_alfresco.sh",

        "sudo bash build_alfresco.sh",

        "curl -sS https://example.com",

        "curl https://example.com",

        "sudo apt-get install -y gcc",

        "apt-get install -y gcc"
    ]

    print("Original commands:")

    for command in test_commands:
        print(command)

    print()

    print("Normalized commands:")

    for command in normalize_commands(
        test_commands
    ):
        print(command)