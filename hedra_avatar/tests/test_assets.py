
import pytest
import requests_mock
from pathlib import Path
from hedra_avatar.core.assets import create_asset, upload_asset

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_create_asset_success(mock_requests):
    mock_requests.post("https://api.hedra.com/v1/assets", json={"id": "test_asset_id"})
    asset_id = create_asset("test_image", "image", "test_api_key")
    assert asset_id == "test_asset_id"

def test_upload_asset_success(mock_requests, tmp_path):
    asset_id = "test_asset_id"
    file_path = tmp_path / "test.jpg"
    file_path.touch()
    mock_requests.put(f"https://api.hedra.com/v1/assets/{asset_id}/upload", status_code=204)
    upload_asset(asset_id, file_path, "test_api_key")
    assert mock_requests.called
