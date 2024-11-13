
run:
	docker compose up
install:
	make migrations
	make migrate
	make superuser
migrations:
	docker compose exec app bash -c "python manage.py makemigrations"
migrate:
	docker compose exec app bash -c "python manage.py migrate"
superuser:
	docker compose exec app bash -c "python manage.py createsuperuser"
shell:
	docker compose run --rm app shell
lint:
	docker compose run --rm app ruff check --fix
test:
	docker compose -f docker-compose.test.yml run --rm test pytest

reset-test-db:
	docker compose -f docker-compose.test.yml down -v --remove-orphans
	docker compose -f docker-compose.test.yml up -d db clickhouse --remove-orphans
	sleep 10  # Give more time for services to start
	docker compose -f docker-compose.test.yml run --rm test python manage.py migrate --no-input
	docker compose -f docker-compose.test.yml run --rm test pytest
