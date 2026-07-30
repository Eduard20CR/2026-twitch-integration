Server:

uv run uvicorn apps.api.main:app --reload

Worker:

uv run -m apps.eventsub_worker

Docker compose:

docker compose up -d