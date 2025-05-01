.PHONY: generate test install-hooks

test:
	pytest

install-hooks:
	pre-commit install