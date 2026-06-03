frontend:
	cd frontend && pnpm run dev

backend:
	cd backend && python app.py

test:
	pytest

build:
	docker compose build
