from importlib.metadata import distributions
from pathlib import Path


def get_requirement_names(file_path: str) -> set[str]:
    names = set()

    for line in Path(file_path).read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        package_name = (
            line.split("==")[0]
            .split(">=")[0]
            .split("<=")[0]
            .split("~=")[0]
            .strip()
            .lower()
        )

        names.add(package_name)

    return names


installed_packages = {
    distribution.metadata["Name"].lower()
    for distribution in distributions()
    if distribution.metadata["Name"]
}

listed_packages = get_requirement_names("requirements.txt")

missing_from_requirements = installed_packages - listed_packages

print("Installed packages not listed in Requirement.txt:")
print("-" * 50)

for package in sorted(missing_from_requirements):
    print(package)
    