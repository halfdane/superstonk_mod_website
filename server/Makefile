SHELL := /bin/bash

.PHONY: dev production test clean setup
dev: setup
	$(VENV)/flask --app "modwebsite:create_app" --debug run

production: setup
	FLASK_APP=modwebsite FLASK_DEBUG=1 $(VENV)/flask run
	#$(VENV)/waitress-serve --call 'scad:create_app'

test: setup
	$(VENV)/pytest -vv

clean: clean-venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
	rm -rf .pytest_cache

setup: venv

include Makefile.venv