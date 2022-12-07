SHELL := /bin/bash

.PHONY: dev production test clean setup
dev: setup
	$(VENV)/quart --env development --app "modwebsite.app:create" run

production: setup
	$(VENV)/quart --env live --app "modwebsite.app:create" run
	#$(VENV)/waitress-serve --call 'scad:create_app'

test: setup
	$(VENV)/pytest -vv

clean: clean-venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
	rm -rf .pytest_cache

setup: venv

include Makefile.venv