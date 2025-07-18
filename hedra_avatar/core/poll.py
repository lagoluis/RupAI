
import time
from pathlib import Path
import requests
from tqdm import tqdm

def wait_and_download(
    generation_id: str, out_dir: Path, api_key: str, timeout: int = 300
) -> Path:
    """Waits for a generation to complete and downloads the result.

    Polls the generation status every 5 seconds until it is complete, failed,
    or the timeout is reached. If successful, it downloads the video file.

    Args:
        generation_id: The ID of the generation to poll.
        out_dir: The directory to save the downloaded file.
        api_key: Your Hedra API key.
        timeout: The maximum time to wait in seconds.

    Returns:
        The path to the downloaded video file.

    Raises:
        TimeoutError: If the generation does not complete within the timeout.
        ValueError: If the generation fails.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        url = f"https://api.hedra.com/v1/generations/{generation_id}/status"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status = response.json()["status"]

        if status == "complete":
            video_url = response.json()["video_url"]
            video_response = requests.get(video_url, stream=True)
            video_response.raise_for_status()

            out_dir.mkdir(exist_ok=True)
            file_path = out_dir / f"{generation_id}.mp4"

            with open(file_path, "wb") as f, tqdm(
                desc=file_path.name,
                total=int(video_response.headers.get("content-length", 0)),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
            return file_path

        if status == "failed":
            raise ValueError("Generation failed.")

        time.sleep(5)

    raise TimeoutError("Timed out waiting for generation to complete.")
