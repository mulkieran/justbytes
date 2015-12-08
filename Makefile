TOX=tox

.PHONY: lint
lint:
	$(TOX) -c tox.ini -e lint

.PHONY: coverage
coverage:
	$(TOX) -c tox.ini -e coverage
	coveralls

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
