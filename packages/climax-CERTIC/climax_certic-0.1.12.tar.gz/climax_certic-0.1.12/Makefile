install:  ## Installation en développement, à n'exécuter qu'une fois
	uv sync
	uv run pre-commit install
.PHONY:install

locales:  ## générer les fichiers de traductions
	msgfmt -o src/climax/locales/fr/LC_MESSAGES/messages.mo src/climax/locales/fr/LC_MESSAGES/messages.po
	msgfmt -o src/climax/locales/en/LC_MESSAGES/messages.mo src/climax/locales/en/LC_MESSAGES/messages.po
.PHONY:locales

clean:
	rm -rf dist
	rm -rf build
.PHONY:clean

build:locales  ## construire le paquet
	uv run pyinstaller src/climax.py --strip --noconfirm --collect-submodules shellingham --collect-submodules urllib
	mkdir dist/climax/_internal/climax
	mkdir dist/climax/_internal/climax/locales
	cp -r src/climax/locales/* dist/climax/_internal/climax/locales/
	cp src/env dist/climax/env
	mkdir -p "${HOME}/.climax/"
	cp -r dist/climax/* "${HOME}/.climax/"
.PHONY:build

format: ## Formatage des sources avec Black
	uv run ruff check --fix ./src/
	uv run ruff format ./src/
.PHONY: format

tests: ## Lancer les tests
	uv run python tests.py
.PHONY: tests

help: ## afficher l'aide
	@echo "\nChoisissez une commande. Les choix sont:\n"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-12s\033[m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help
