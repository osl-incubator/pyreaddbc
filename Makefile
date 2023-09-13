# Variables
PYTHON = poetry run python
PYTEST = poetry run pytest
TEST_FILES = tests/data/*.dbf tests/data/*.gz
SEMANTIC_RELEASE = npx --yes \
          -p semantic-release \
          -p conventional-changelog-conventionalcommits \
          -p "@semantic-release/commit-analyzer" \
          -p "@semantic-release/release-notes-generator" \
          -p "@semantic-release/changelog" \
          -p "@semantic-release/exec" \
          -p "@semantic-release/github" \
          -p "@semantic-release/git" \
          -p "semantic-release-replace-plugin" \
          semantic-release


.PHONY: install
install:
	mamba env create -f conda/dev.yaml 
	poetry install


.PHONY: test
test:
	$(PYTEST) -vv -k "ZIKABR21 or STPI2206 or sids" tests/


.PHONY: clean-build
clean-build: ## Remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	@find . -name '*.cache' -exec rm -fr {} +
	@find . -name '*.jupyter' -exec rm -fr {} +
	@find . -name '*.local' -exec rm -fr {} +
	@find . -name '*.mozilla' -exec rm -fr {} +
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.ipynb_checkpoints' -exec rm -rf {} +


.PHONY: clean-pyc
clean-pyc: ## Remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +


.PHONY: clean-test
clean-test: ## Remove tests databases
	@find ./ -name '*.dbf' -exec rm -f {} \;
	@find ./ -name '*csv.gz' -exec rm -f {} \;
	@find ./ -name '*.pytest_cache' -exec rm -rf {} \;


.PHONY: release
release: ## Make release
	$(SEMANTIC_RELEASE) --ci


.PHONY: release-dry
release-dry: ## Test make release
	$(SEMANTIC_RELEASE) --dry-run
