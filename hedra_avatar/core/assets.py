
from pathlib import Path
from typing import Literal

import requests

def create_asset(name: str, kind: Literal['image', 'audio'], api_key: str) -> str:
    """Creates a new asset in Hedra.

    Args:
        name: The name of the asset.
        kind: The type of asset, either 'image' or 'audio'.
        api_key: Your Hedra API key.

    Returns:
        The ID of the newly created asset.
    """
    url = "https://api.hedra.com/v1/assets"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"name": name, "kind": kind}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["id"]

def upload_asset(asset_id: str, file: Path, api_key: str) -> None:
    """Uploads a file to an existing asset.

    Args:
        asset_id: The ID of the asset to upload to.
        file: The path to the file to upload.
        api_key: Your Hedra API key.
    """
    url = f"https://api.hedra.com/v1/assets/{asset_id}/upload"
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(file, "rb") as f:
        response = requests.put(url, headers=headers, data=f)
        response.raise_for_status()
