install:
	uv pip install -r requirements.txt

run:
	python -m hedra_avatar

lint:
	uv run ruff check .

test:
	uv run pytest
