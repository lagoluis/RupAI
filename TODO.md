TODO.md – Hedra Avatar Pipeline

Task List
	✓	P01_INIT – Initialize project skeleton
See prompt P01_INIT below.
	✓	P02_ASSET – Build asset-upload module (create_asset, upload_asset)
See prompt P02_ASSET.
	✓	P03_GEN – Build generation module (start_generation, model-ID helper)
See prompt P03_GEN.
	✓	P04_POLL – Build polling / downloader module (wait_and_download)
See prompt P04_POLL.
	✓	P05_CLI – Build CLI entry-point
See prompt P05_CLI.
	✓	P06_WATCH – Add file-watcher integration
See prompt P06_WATCH.
	•	P07_UTIL – Error handling & credits-check utilities
See prompt P07_UTIL.

⸻

Prompts

P01_INIT

You are an expert Python backend developer working on macOS.

Goal: initialize the project skeleton for the Hedra Avatar pipeline.

Requirements:
- Create directory structure:

  hedra_avatar/
      __init__.py
      core/
          __init__.py
      tests/
      output/
  .env.example

- Target Python 3.11; add a `.python-version` file.
- Dependency management: provide `uv`-friendly `requirements.txt` containing: python-dotenv, requests, tqdm, watchdog.
- Provide `Makefile` with targets: **install**, **run** (CLI example), **lint** (ruff), **test** (pytest).
- Provide a concise **README.md** “Getting started” section.

Do **not** implement application logic yet—focus on scaffolding. Output file contents ready to be written to disk.

P02_ASSET

Implement `hedra_avatar/core/assets.py` with:

- `create_asset(name: str, kind: Literal['image','audio'], api_key: str) -> str`
- `upload_asset(asset_id: str, file: Path, api_key: str) -> None`

Use **requests** with `raise_for_status`. Add rich doc-strings and type hints.
Write unit tests in `tests/test_assets.py` using **pytest** and **requests-mock**.
Return the full file contents and the new tests.

P03_GEN

Create `hedra_avatar/core/generation.py` containing:

- `get_default_model_id(api_key: str) -> str`
  • Try env-var `HEDRA_MODEL_ID`; if absent call `/models` and choose the first entry where `ai_model_type == character-3` and status is ACTIVE; cache to `.cache/model_id`.

- `start_generation(image_id: str, audio_id: str, prompt: str, api_key: str, model_id: str | None = None) -> str`
  • Build payload per Hedra docs, resolution 540p, 9:16 aspect ratio.

Include unit tests mocking HTTP.

P04_POLL

Implement `hedra_avatar/core/poll.py` with:

- `wait_and_download(generation_id: str, out_dir: Path, api_key: str, timeout: int = 300) -> Path`

Poll `GET /generations/{id}/status` every 5 s until **complete**, **failed**, or timeout.
Stream-download the MP4 using **tqdm**; return local path.
Add tests with **pytest** & **freezegun** to cover timeout branch.

P05_CLI

Add `hedra_avatar/__main__.py`:

- Arg-flags `--wav`, `--img`, `--prompt` (optional).
- Load `.env`, read `HEDRA_API_KEY`.
- Wire calls: assets → generation → wait → print output.
- On exception print a user-friendly message and exit 1.

Expose entry-point via **pyproject.toml**:

[project.scripts]
hedra-avatar = 'hedra_avatar.__main__:cli'

Create smoke test.

P06_WATCH

Implement `hedra_avatar/watch.py`:

- Monitor `incoming/` for new `.wav` files using **watchdog** `Observer`.
- Use constant env-var `FRIEND_IMG` for image path.
- Debounce duplicate events; enqueue to a thread-pool to run the pipeline.
- Log progress with **rich**.

Add a systemd-user service example to README.

P07_UTIL

Enhance robustness:

- `hedra_avatar/core/utils.py`:
  • `get_credit_balance(api_key) -> int`
  • Decorator `retry(exceptions, tries=3, delay=2, backoff=2)`.

Refactor other modules to import utilities.
Add tests covering retries and low-credit error paths.