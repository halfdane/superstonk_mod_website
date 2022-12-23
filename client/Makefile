SHELL := /bin/bash

.PHONY: dev production test clean setup bot
dev: setup
	npm run dev

bot:
	echo "Nothing to do here"

production: setup
	npm run build

test: setup
	npm run test

clean:
	rm node_modules

setup: node_modules

node_modules:
	npm install

