SHELL := /bin/bash


server:
	@FLASK_APP=slack_g_cal/server/server.py flask run --host=0.0.0.0

server-dev:
	@FLASK_DEBUG=1 FLASK_APP=slack_g_cal/server/server.py flask run --host=0.0.0.0

queue:
	celery -A slack_g_cal.queue worker -l info

setup:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "===================================================="; \
		echo "Please activate the appropriate virtual environment"; \
		echo "===================================================="; \
		exit 1; \
	fi
	pip install -r requirements.txt
