
import pytest
import requests_mock
from freezegun import freeze_time
from pathlib import Path
from hedra_avatar.core.poll import wait_and_download

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_wait_and_download_success(mock_requests, tmp_path):
    generation_id = "gen_id"
    out_dir = tmp_path / "output"
    mock_requests.get(
        f"https://api.hedra.com/v1/generations/{generation_id}/status",
        [
            {"json": {"status": "processing"}},
            {"json": {"status": "complete", "video_url": "https://example.com/video.mp4"}},
        ],
    )
    mock_requests.get("https://example.com/video.mp4", content=b"video_content")

    result_path = wait_and_download(generation_id, out_dir, "api_key")

    assert result_path == out_dir / f"{generation_id}.mp4"
    assert result_path.read_bytes() == b"video_content"

def test_wait_and_download_failed(mock_requests, tmp_path):
    generation_id = "gen_id"
    out_dir = tmp_path / "output"
    mock_requests.get(
        f"https://api.hedra.com/v1/generations/{generation_id}/status",
        json={"status": "failed"},
    )

    with pytest.raises(ValueError, match="Generation failed."):
        wait_and_download(generation_id, out_dir, "api_key")

@freeze_time("2025-07-18")
def test_wait_and_download_timeout(mock_requests, tmp_path):
    generation_id = "gen_id"
    out_dir = tmp_path / "output"
    mock_requests.get(
        f"https://api.hedra.com/v1/generations/{generation_id}/status",
        json={"status": "processing"},
    )

    with pytest.raises(TimeoutError):
        wait_and_download(generation_id, out_dir, "api_key", timeout=10)
