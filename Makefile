# Variables
PYTHON = poetry run python
PYTEST = poetry run pytest
TEST_FILES = tests/data/*.dbf tests/data/*.gz

# Targets
.PHONY: install clean test

install:
	mamba env create -f conda/dev.yaml 
	poetry install

test:
	$(PYTEST) -vv -k "ZIKABR21 or STPI2206 or sids" tests/

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*.pyo' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@find ./ -name '*.dbf' -exec rm -f {} \;
	@find ./ -name '*csv.gz' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
