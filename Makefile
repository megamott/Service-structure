start:
	poetry run gunicorn app:create_app --bind=localhost:8000 --worker-class aiohttp.GunicornWebWorker --reload -w 6 --timeout=7200

migrate:
	poetry run alembic upgrade head

test:
	poetry run coverage run --source='.' -m pytest -v tests

report:
	poetry run coverage report

ruff:
	poetry run ruff check app/

black:
	poetry run black app/

isort:
	poetry run isort app/

format:
	make black && make isort

lint:
	poetry run isort app/ -c
	poetry run black app/ --check
	poetry run ruff check app/

requirements-prd:
	poetry export --without-hashes --format requirements.txt > etc/requirements.txt

requirements-dev:
	poetry export --without-hashes --format requirements.txt --only dev > etc/requirements-dev.txt