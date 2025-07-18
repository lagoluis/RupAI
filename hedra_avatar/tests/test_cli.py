
import subprocess
import sys
from pathlib import Path

def test_cli_smoke():
    """Smoke test for the CLI entry point."""
    wav_path = Path(__file__).parent / "smoke_test_data" / "test.wav"
    img_path = Path(__file__).parent / "smoke_test_data" / "test.jpg"

    # This is a smoke test, so we don't expect it to actually succeed
    # in a CI environment without a real API key. We just want to ensure
    # it runs without crashing and exits with a non-zero status code
    # because the API key is missing.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "hedra_avatar",
            "--wav",
            str(wav_path),
            "--img",
            str(img_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "HEDRA_API_KEY not found" in result.stderr
