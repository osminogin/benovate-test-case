WSGI_PROCESSES ?= 4
MAX_REQUESTS ?= 1200

run:
	@pipenv run ./manage.py runserver

migrations:
	@pipenv run ./manage.py makemigrations && pipenv run ./manage.py migrate

server:
	@pipenv run gunicorn -w $(WSGI_PROCESSES) --max-requests $(MAX_REQUESTS) benovate.wsgi --log-file -

test:
	@pipenv run flake8
	@pipenv run pytest


.PHONY: run server migrations test
