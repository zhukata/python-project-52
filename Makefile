install:
	poetry install

test:
	poetry run python manage.py test --verbosity 2

test-coverage:
	coverage run --source='.' manage.py test
	coverage xml

lint:
	poetry run flake8 task_manager

dev:
	poetry run python manage.py runserver

start:
	poetry run gunicorn task_manager.wsgi

migrate:
	poetry run python manage.py migrate

makemigrate:
	poetry run python manage.py makemigrations

build:
	./build.sh