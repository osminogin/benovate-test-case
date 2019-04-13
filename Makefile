PROJECT_NAME ?= benovate-test-case
WSGI_PROCESSES ?= 5
MAX_REQUESTS ?= 1200

run:
	@pipenv run ./manage.py runserver

migrations:
	@pipenv run ./manage.py makemigrations && pipenv run ./manage.py migrate

build:
	@docker build -t $(PROJECT_NAME) .

server:
	@pipenv run gunicorn --workers $(WSGI_PROCESSES) \
		--max-requests $(MAX_REQUESTS) \
		--bind 0.0.0.0:9000 \
	 	--log-file - \
		benovate.wsgi

test:
	@pipenv run flake8
	@pipenv run pytest


.PHONY: run server migrations test build
