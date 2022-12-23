SHELL := /bin/bash

.PHONY: dev production test clean setup
dev: setup
	npm run dev

production: setup
	npm run build

build: production
	tar -czvf client.tgz dist

test: setup
	npm run test

clean:
	rm node_modules

setup: node_modules

node_modules:
	npm install

