# general
MANAGE=manage.py
COVERAGE=coverage
COVER=apps

DOCKER_COMPOSE=docker-compose
DOCKER_DEV_CONFIG=docker-compose.yml
CELERY_CONFIG=config.celery_app

celery:
	celery -A $(CELERY_CONFIG) worker -l info

static:
	python3 manage.py collectstatic --noinput

flower:
	flower -A $(CELERY_CONFIG) --port=5555

docker_stop:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) stop

docker_start:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) up

docker_rebuild:
	$(DOCKER_COMPOSE) -f $(DOCKER_DEV_CONFIG) up --build

migrate:
	python3 manage.py migrate

install_devs:
	pip3 install -r requirements_dev.txt

install_prods:
	pip3 install -r requirements.txt

run_server:
	python3 manage.py runserver 192.168.100.124:8000

run_gunicorn:
	inv run_it
