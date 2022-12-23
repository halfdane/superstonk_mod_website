SHELL := /bin/bash

.PHONY: dev production test clean setup force_pull bot
# use to run the dev client with the dev server
dev: setup
	QUART_ENV=development $(VENV)/quart --app "modwebsite.app:create" run

# use to run the static client with the dev server
prelive: setup
	QUART_ENV=prelive $(VENV)/quart --debug --app "modwebsite.app:create" run

production: setup
	QUART_ENV=live $(VENV)/hypercorn "modwebsite.app:app" --bind 0.0.0.0:3000

force_pull:
	git fetch --all
	git reset --hard origin/main
	git pull --rebase

bot: force_pull production

test: setup
	$(VENV)/pytest -vv

clean: clean-venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete
	rm -rf .pytest_cache

setup: venv

include Makefile.venv