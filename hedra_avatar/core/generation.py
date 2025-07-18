
import os
from pathlib import Path
import requests
from hedra_avatar.core.utils import retry

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)
MODEL_ID_CACHE = CACHE_DIR / "model_id"

@retry(requests.exceptions.RequestException)
def get_default_model_id(api_key: str) -> str:
    """Gets the default model ID from cache or Hedra API.

    Tries to read the model ID from the HEDRA_MODEL_ID environment variable first.
    If not found, it checks for a cached model ID in .cache/model_id.
    If not cached, it fetches the models from the Hedra API, chooses the first
    active character-3 model, and caches the ID.

    Args:
        api_key: Your Hedra API key.

    Returns:
        The default model ID.
    """
    if "HEDRA_MODEL_ID" in os.environ:
        return os.environ["HEDRA_MODEL_ID"]

    if MODEL_ID_CACHE.exists():
        return MODEL_ID_CACHE.read_text()

    url = "https://api.hedra.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    for model in response.json():
        if model.get("ai_model_type") == "character-3" and model.get("status") == "ACTIVE":
            model_id = model["id"]
            MODEL_ID_CACHE.write_text(model_id)
            return model_id

    raise ValueError("No suitable model found.")

@retry(requests.exceptions.RequestException)
def start_generation(
    image_id: str,
    audio_id: str,
    prompt: str,
    api_key: str,
    model_id: str | None = None,
) -> str:
    """Starts a new video generation task.

    Args:
        image_id: The ID of the image asset.
        audio_id: The ID of the audio asset.
        prompt: The prompt for the generation.
        api_key: Your Hedra API key.
        model_id: The model ID to use. If None, the default is used.

    Returns:
        The ID of the generation task.
    """
    if model_id is None:
        model_id = get_default_model_id(api_key)

    url = "https://api.hedra.com/v1/generations"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model_id": model_id,
        "prompt": prompt,
        "image_id": image_id,
        "audio_id": audio_id,
        "resolution": "540p",
        "aspect_ratio": "9:16",
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]
