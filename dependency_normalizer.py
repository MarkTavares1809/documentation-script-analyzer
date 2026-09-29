import re


def normalize_dependency(package):

    package = package.lower().strip()

    # -----------------------------------
    # GCC
    # -----------------------------------

    if re.match(r"^gcc(?:-\d+)?$", package):
        return "gcc"

    # -----------------------------------
    # G++
    # -----------------------------------

    if re.match(r"^g\+\+(?:-\d+)?$", package):
        return "g++"

    # -----------------------------------
    # Clang
    # -----------------------------------

    if re.match(r"^clang(?:-\d+)?$", package):
        return "clang"

    # -----------------------------------
    # Clang tools
    # -----------------------------------

    if re.match(
        r"^clang-tools(?:-\d+)?$",
        package
    ):
        return "clang-tools"

    # -----------------------------------
    # OpenJDK
    # -----------------------------------

    if (
        package == "java"
        or package == "openjdk"
        or package.startswith("openjdk-")
    ):
        return "openjdk"

    # -----------------------------------
    # Python
    # -----------------------------------

    if re.match(
        r"^python(?:3(?:\.\d+)?)?$",
        package
    ):
        return "python"

    # -----------------------------------
    # Maven
    # -----------------------------------

    if package == "maven":
        return "maven"

    # -----------------------------------
    # Go
    # -----------------------------------

    if (
        package == "golang"
        or package.startswith("golang-")
    ):
        return "golang"

    # -----------------------------------
    # CMake
    # -----------------------------------

    if package == "cmake":
        return "cmake"

    # -----------------------------------
    # Git
    # -----------------------------------

    if package == "git":
        return "git"

    # -----------------------------------
    # Curl
    # -----------------------------------

    if package == "curl":
        return "curl"

    # -----------------------------------
    # Wget
    # -----------------------------------

    if package == "wget":
        return "wget"

    # -----------------------------------
    # Make
    # -----------------------------------

    if package in [
        "make",
        "build-essential"
    ]:
        return "make"

    # -----------------------------------
    # Protobuf
    # -----------------------------------

    if (
        package == "protobuf"
        or package.startswith("protobuf-")
    ):
        return "protobuf"

    # -----------------------------------
    # Zip
    # -----------------------------------

    if package == "zip":
        return "zip"

    # -----------------------------------
    # Unzip
    # -----------------------------------

    if package == "unzip":
        return "unzip"

    # -----------------------------------
    # Netty
    # -----------------------------------

    if package.startswith("netty"):
        return "netty"

    # -----------------------------------
    # Zlib
    # -----------------------------------

    if package.startswith("zlib"):
        return "zlib"

    # -----------------------------------
    # Everything else
    # -----------------------------------

    return package


def normalize_dependencies(
    dependencies
):

    normalized = []

    for dependency in dependencies:

        normalized_dependency = (
            normalize_dependency(
                dependency
            )
        )

        normalized.append(
            normalized_dependency
        )

    return sorted(
        set(normalized)
    )


# -----------------------------------
# Test
# -----------------------------------

if __name__ == "__main__":

    test_dependencies = [

        "gcc",
        "gcc-11",
        "gcc-13",

        "g++",
        "g++-11",
        "g++-13",

        "openjdk",
        "openjdk-17-jdk",
        "openjdk-21-jdk-headless",

        "python",
        "python3",

        "clang",
        "clang-tools-18",

        "build-essential",
        "cmake",
        "git"
    ]

    print(
        "Original dependencies:"
    )

    print(
        test_dependencies
    )

    print()

    print(
        "Normalized dependencies:"
    )

    print(
        normalize_dependencies(
            test_dependencies
        )
    )