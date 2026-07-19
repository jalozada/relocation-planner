import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_BUILD_DIR = BASE_DIR / "static" / "build"


def copy_asset(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def main() -> None:
    STATIC_BUILD_DIR.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            str(BASE_DIR / "tools" / "tailwindcss"),
            "-i",
            str(BASE_DIR / "assets" / "css" / "app.css"),
            "-o",
            str(STATIC_BUILD_DIR / "app.css"),
            "--minify",
        ],
        check=True,
    )

    copy_asset(BASE_DIR / "assets" / "js" / "app.js", STATIC_BUILD_DIR / "app.js")
    copy_asset(BASE_DIR / "assets" / "vendor" / "htmx.min.js", STATIC_BUILD_DIR / "htmx.min.js")
    copy_asset(BASE_DIR / "assets" / "vendor" / "alpine.min.js", STATIC_BUILD_DIR / "alpine.min.js")
    copy_asset(BASE_DIR / "assets" / "vendor" / "lucide.min.js", STATIC_BUILD_DIR / "lucide.min.js")


if __name__ == "__main__":
    main()
