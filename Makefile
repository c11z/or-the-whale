.PHONY: build run format check

IMAGE=great_illustrated_classic:latest

build:
	@docker build \
		--quiet \
		--tag=$(IMAGE) \
		.

format: build
	@docker run \
		--rm \
		--volume $(CURDIR)/main.py:/script/main.py \
		$(IMAGE) \
		black --quiet /script/main.py

check: format
	@docker run \
		--rm \
		--volume $(CURDIR)/main.py:/script/main.py \
		$(IMAGE) \
		mypy /script/main.py

run: format 
	@docker run \
		--rm \
		--volume $(CURDIR)/main.py:/script/main.py \
		--volume $(CURDIR)/data:/script/data \
		$(IMAGE) \
		python3 /script/main.py

console: build
	@docker run \
		--rm \
		--tty \
		--interactive \
		--volume $(CURDIR)/main.py:/script/main.py \
		--volume $(CURDIR)/data:/script/data \
		--workdir /script \
		$(IMAGE) \
		/bin/bash
