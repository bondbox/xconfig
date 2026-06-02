MAKEFLAGS += --always-make

VERSION := $(shell python3 -c "from tomllib import load; print(load(open('.xproject_python', 'rb'))['version'])")
SUBDIRS := xconfig xconfig-attr xconfig-file xconfig-toml xconfig-yaml

all: build test


release: all
	if [ -n "${VERSION}" ]; then \
		git tag -a v${VERSION} -m "release v${VERSION}"; \
		git push origin --tags; \
	fi

version:
	@echo ${VERSION}


build:
	for dir in $(SUBDIRS); do \
		make -C $$dir build; \
	done


clean:
	for dir in $(SUBDIRS); do \
		make -C $$dir clean; \
	done


test:
	for dir in $(SUBDIRS); do \
		make -C $$dir test; \
	done


install:
	for dir in $(SUBDIRS); do \
		make -C $$dir install; \
	done


uninstall:
	for dir in $(SUBDIRS); do \
		make -C $$dir uninstall; \
	done


reinstall:
	for dir in $(SUBDIRS); do \
		make -C $$dir reinstall; \
	done
