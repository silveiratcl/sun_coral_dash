from __future__ import annotations

from importlib import metadata
from pathlib import Path
import re
import sys


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, ValueError):
            continue
    return raw.decode("latin-1")


def parse_requirements(path: Path) -> dict[str, str]:
    reqs: dict[str, str] = {}
    for raw in _read_text(path).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            continue

        # Only enforce exact pins to keep checks deterministic.
        match = re.match(r"^([A-Za-z0-9_.-]+)==([^\s]+)$", line)
        if match:
            name = match.group(1)
            version = match.group(2)
            reqs[name.lower()] = version
    return reqs


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    req_path = repo_root / "requirements.txt"

    if not req_path.exists():
        print("ERROR: requirements.txt not found.")
        return 2

    required = parse_requirements(req_path)
    if not required:
        print("WARNING: No exact pinned packages found in requirements.txt.")
        return 0

    missing: list[str] = []
    mismatched: list[tuple[str, str, str]] = []

    for pkg_name, required_version in sorted(required.items()):
        try:
            installed_version = metadata.version(pkg_name)
        except metadata.PackageNotFoundError:
            missing.append(pkg_name)
            continue

        if installed_version != required_version:
            mismatched.append((pkg_name, required_version, installed_version))

    if missing or mismatched:
        print("Environment check failed.")

        if missing:
            print("Missing packages:")
            for pkg in missing:
                print(f" - {pkg}")

        if mismatched:
            print("Version mismatches:")
            for pkg, required_version, installed_version in mismatched:
                print(f" - {pkg}: required {required_version}, installed {installed_version}")

        print("Run: .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return 1

    print("Environment check OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
