
import pytest
import requests_mock
from hedra_avatar.core.generation import get_default_model_id, start_generation

@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m

def test_get_default_model_id_from_env(mock_requests, monkeypatch):
    monkeypatch.setenv("HEDRA_MODEL_ID", "env_model_id")
    assert get_default_model_id("test_api_key") == "env_model_id"

def test_get_default_model_id_from_cache(mock_requests, tmp_path):
    cache_file = tmp_path / ".cache" / "model_id"
    cache_file.parent.mkdir()
    cache_file.write_text("cached_model_id")
    with pytest.MonkeyPatch.context() as m:
        m.chdir(tmp_path)
        assert get_default_model_id("test_api_key") == "cached_model_id"

def test_get_default_model_id_from_api(mock_requests, tmp_path):
    with pytest.MonkeyPatch.context() as m:
        m.chdir(tmp_path)
        mock_requests.get(
            "https://api.hedra.com/v1/models",
            json=[
                {"id": "model1", "ai_model_type": "other", "status": "ACTIVE"},
                {"id": "model2", "ai_model_type": "character-3", "status": "INACTIVE"},
                {"id": "model3", "ai_model_type": "character-3", "status": "ACTIVE"},
            ],
        )
        model_id = get_default_model_id("test_api_key")
        assert model_id == "model3"
        assert (tmp_path / ".cache" / "model_id").read_text() == "model3"

def test_start_generation(mock_requests):
    mock_requests.post("https://api.hedra.com/v1/generations", json={"id": "gen_id"})
    generation_id = start_generation(
        "img_id", "aud_id", "prompt", "api_key", model_id="model_id"
    )
    assert generation_id == "gen_id"
