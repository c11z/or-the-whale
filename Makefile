APP_NAME=main
IMAGE_TAG=or_the_whale:latest
MAINTAINER=me@c11z.com
ARGS?="noop"

include python.mk

check: format
	@docker run \
		--rm \
		--user $(UGID) \
		--volume $(CURDIR):/script \
		$(IMAGE_TAG) \
		python3 -m mypy --ignore-missing-imports /script

call: build_quiet
	@docker run \
		--rm \
		--user $(UGID) \
		--volume $(CURDIR):/script \
		$(IMAGE_TAG) \
		python3 /script/$(APP_NAME).py $(ARGS)
