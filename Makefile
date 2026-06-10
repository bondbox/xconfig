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

OPTIONS := build clean test install uninstall reinstall
TARGETS := $(foreach op,$(OPTIONS),$(foreach dir,$(SUBDIRS),$(op)-$(dir)))

.PHONY: $(TARGETS)

$(TARGETS):
	@$(eval OP := $(firstword $(subst -, ,$@)))
	@$(eval DIR := $(word 2,$(subst -, ,$@)))
	@echo "Running '$(OP)' in '$(DIR)'..."
	@make -C $(DIR) $(OP)

build: $(foreach dir,$(SUBDIRS),build-$(dir))

clean: $(foreach dir,$(SUBDIRS),clean-$(dir))

test: $(foreach dir,$(SUBDIRS),test-$(dir))

install: $(foreach dir,$(SUBDIRS),install-$(dir))

uninstall: $(foreach dir,$(SUBDIRS),uninstall-$(dir))

reinstall: $(foreach dir,$(SUBDIRS),reinstall-$(dir))
