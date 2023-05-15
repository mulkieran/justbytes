.PHONY: lint
lint:
	pylint setup.py
	pylint src/justbytes
	pylint tests --disable=unnecessary-dunder-call

.PHONY: test
test:
	python3 -m unittest discover --verbose tests

.PHONY: coverage
coverage:
	coverage --version
	coverage run --timid --branch -m unittest discover tests/
	coverage report -m --fail-under=98 --show-missing --include="./src/*"

.PHONY: fmt
fmt:
	isort setup.py src tests --skip src/justbytes/__init__.py
	black .

.PHONY: fmt-travis
fmt-travis:
	isort --diff --check-only setup.py src tests --skip src/justbytes/__init__.py
	black . --check

PYREVERSE_OPTS = --output=pdf
.PHONY: view
view:
	-rm -Rf _pyreverse
	mkdir _pyreverse
	PYTHONPATH=src pyreverse ${PYREVERSE_OPTS} --project="justbytes" src/justbytes
	mv classes_justbytes.pdf _pyreverse
	mv packages_justbytes.pdf _pyreverse

.PHONY: docs
docs:
	cd doc/_build/html; zip -r ../../../docs *

.PHONY: yamllint
yamllint:
	yamllint --strict .github/workflows/*.yml

.PHONY: package
package:
	(umask 0022; python -m build; python -m twine check --strict ./dist/*)

.PHONY: legacy-package
legacy-package:
	python3 setup.py build
	python3 setup.py install
