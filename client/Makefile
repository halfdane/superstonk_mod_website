SHELL := /bin/bash

.PHONY: dev production test clean setup
dev: setup
	npm run serve

production: setup
	npm run build

clean:
	rm -rf dist
	rm -rf node_modules

setup:
	npm install
