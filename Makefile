.PHONY: generate test install-hooks

generate:
	./scripts/generate_models.sh

test:
	pytest

install-hooks:
	pre-commit install