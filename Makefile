.PHONY: build install dist sources srpm rpm pypi clean

PYTHON        ?= python
INSTALL_FLAGS ?=

NAME          := psys
RPM_NAME      := python-$(NAME)
VERSION       := $(shell $(PYTHON) setup.py --version)

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install --skip-build $(INSTALL_FLAGS)

dist: clean
	$(PYTHON) setup.py sdist
	mv dist/$(NAME)-*.tar.gz .

sources:
	@git archive --format=tar --prefix="$(NAME)-$(VERSION)/" \
		$(shell git rev-parse --verify HEAD) | gzip > $(NAME)-$(VERSION).tar.gz

srpm: dist
	rpmbuild -bs --define "_sourcedir $(CURDIR)" $(RPM_NAME).spec

rpm: dist
	rpmbuild -ba --define "_sourcedir $(CURDIR)" $(RPM_NAME).spec

pypi: clean
	$(PYTHON) setup.py sdist upload

clean:
	rm -rf build dist $(NAME)-*.tar.gz $(NAME).egg-info
