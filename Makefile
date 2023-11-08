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