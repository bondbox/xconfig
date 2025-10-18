MAKEFLAGS += --always-make

VERSION := $(shell python3 setup_config.py --version)

all: build reinstall test


release: all
	git tag -a v${VERSION} -m "release v${VERSION}"
	git push origin --tags


clean-cover:
	rm -rf cover .coverage coverage.xml htmlcov
clean-tox:
	rm -rf .stestr .tox
clean: build-clean test-clean clean-cover clean-tox


upload:
	python3 -m pip install --upgrade xpip-upload
	xpip-upload --config-file .pypirc dist/*


build-prepare:
	python3 -m pip install --upgrade -r requirements.txt
	python3 -m pip install --upgrade xpip-build
build-clean:
	xpip-build --debug setup --clean
build: build-prepare build-clean
	xpip-build --debug setup --all --file setup_config.py
	xpip-build --debug setup --all --file setup_config_attrs.py
	xpip-build --debug setup --all --file setup_config_file.py
	xpip-build --debug setup --all --file setup_config_toml.py
	xpip-build --debug setup --all --file setup_config_yaml.py


install:
	python3 -m pip install --force-reinstall --no-deps dist/*.whl
uninstall:
	python3 -m pip uninstall -y xkits-config xkits-config-file
reinstall: uninstall install


test-prepare:
	python3 -m pip install --upgrade mock pylint flake8 pytest pytest-cov
pylint:
	pylint $(shell git ls-files xkits_config*.py)
flake8:
	flake8 xkits_config*.py --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 xkits_config*.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest --cov=xkits_config_annot --cov=xkits_config_attrs --cov=xkits_config_class --cov=xkits_config_file --cov=xkits_config_json  --cov=xkits_config_toml --cov=xkits_config_yaml --cov=xkits_config --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-clean:
	rm -rf .pytest_cache
test: test-prepare pylint flake8 pytest
test-clean: pytest-clean
