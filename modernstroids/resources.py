from pathlib import Path

ASSET_DIRECTORY = Path(__file__).resolve().parent.parent / "assets"


def get_asset_path(*parts: str) -> Path:
    return ASSET_DIRECTORY.joinpath(*parts)
