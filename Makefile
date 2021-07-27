TOX=tox

.PHONY: lint
lint:
	$(TOX) -c tox.ini -e lint

.PHONY: coverage
coverage:
	$(TOX) -c tox.ini -e coverage

.PHONY: fmt
fmt:
	isort setup.py src tests --skip src/justbytes/__init__.py
	black .

.PHONY: fmt-travis
fmt-travis:
	isort --diff --check-only setup.py src tests --skip src/justbytes/__init__.py
	black . --check

.PHONY: test
test:
	$(TOX) -c tox.ini -e test

PYREVERSE_OPTS = --output=pdf
.PHONY: view
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=src pyreverse ${PYREVERSE_OPTS} --project="justbytes" src/justbytes
	mv classes_justbytes.pdf _pyreverse
	mv packages_justbytes.pdf _pyreverse

.PHONY: archive
archive:
	git archive --output=./justbytes.tar.gz HEAD

.PHONY: upload-release
upload-release:
	python setup.py register sdist upload

.PHONY: docs
docs:
	cd doc/_build/html; zip -r ../../../docs *

.PHONY: yamllint
yamllint:
	yamllint --strict .github/workflows/main.yml
