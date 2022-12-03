SHELL := /bin/bash

.PHONY: dev production test clean setup
dev: setup
	FLASK_APP=app FLASK_DEBUG=1 $(VENV)/flask run

production: setup
	FLASK_APP=app FLASK_DEBUG=1 $(VENV)/flask run
	#$(VENV)/waitress-serve --call 'scad:create_app'

test: setup
	$(VENV)/pytest -vv

clean: clean-venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
	rm -rf .pytest_cache

setup: clean venv

include Makefile.venv