MAKEFLAGS += --always-make

VERSION := $(shell python3 xconfig/setup.py --version)

all: build reinstall test


release: all
	if [ -n "${VERSION}" ]; then \
		git tag -a v${VERSION} -m "release v${VERSION}"; \
		git push origin --tags; \
	fi

version:
	@echo ${VERSION}


clean-cover:
	rm -rf cover .coverage coverage.xml htmlcov
clean-tox:
	rm -rf .stestr .tox
clean: build-clean test-clean clean-cover clean-tox


upload:
	python3 -m pip install --upgrade xpip-upload
	xpip-upload --config-file .pypirc xconfig*/dist/*


build-prepare:
	python3 -m pip install --upgrade -r xconfig/requirements.txt
	python3 -m pip install --upgrade -r xconfig_attr/requirements.txt
	python3 -m pip install --upgrade -r xconfig_file/requirements.txt
	python3 -m pip install --upgrade -r xconfig_toml/requirements.txt
	python3 -m pip install --upgrade -r xconfig_yaml/requirements.txt
	python3 -m pip install --upgrade xpip-build
build-clean:
	xpip-build --debug --path xconfig setup --clean
	xpip-build --debug --path xconfig_attr setup --clean
	xpip-build --debug --path xconfig_file setup --clean
	xpip-build --debug --path xconfig_toml setup --clean
	xpip-build --debug --path xconfig_yaml setup --clean
build: build-prepare build-clean
	xpip-build --debug --path xconfig setup --all
	xpip-build --debug --path xconfig_attr setup --all
	xpip-build --debug --path xconfig_file setup --all
	xpip-build --debug --path xconfig_toml setup --all
	xpip-build --debug --path xconfig_yaml setup --all


install:
	python3 -m pip install --force-reinstall --no-deps xconfig*/dist/*.whl
uninstall:
	python3 -m pip uninstall -y xkits-config-attrs
	python3 -m pip uninstall -y xkits-config-yaml
	python3 -m pip uninstall -y xkits-config-toml
	python3 -m pip uninstall -y xkits-config-file
	python3 -m pip uninstall -y xkits-config
reinstall: uninstall install


test-prepare:
	python3 -m pip install --upgrade mock pylint flake8 pytest pytest-cov
pylint:
	pylint $(shell git ls-files xconfig*/xkits_config*.py)
flake8:
	flake8 xconfig* --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 xconfig* --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
pytest:
	pytest --cov=xconfig_yaml --cov=xconfig_toml --cov=xconfig_file --cov=xconfig_attr --cov=xconfig --cov-report=term-missing --cov-report=xml --cov-report=html --cov-config=.coveragerc --cov-fail-under=100
pytest-clean:
	rm -rf .pytest_cache
test: test-prepare pylint flake8 pytest
test-clean: pytest-clean
