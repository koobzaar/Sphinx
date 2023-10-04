from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def show_ascii_art_header() -> None:
    """Print the project header when it is available."""
    header_path = REPO_ROOT / "header"
    if header_path.exists():
        print(header_path.read_text(encoding="utf-8"))


def show_anu_logo() -> None:
    """Print the ANU logo banner when it is available."""
    logo_path = REPO_ROOT / "ANU_logo"
    if logo_path.exists():
        print(logo_path.read_text(encoding="utf-8"))
