PYCODE = import flask.ext.statics as a; print a.__path__[0]
.PHONY: default isvirtualenv

default:
	@echo "Local examples:"
	@echo "    make run        # Starts a Flask development server locally."
	@echo "    make style      # Check code styling with flake8."
	@echo "    make lint       # Runs PyLint."
	@echo "    make test       # Tests entire application with pytest."

isvirtualenv:
	@if [ -z "$(VIRTUAL_ENV)" ]; then echo "ERROR: Not in a virtualenv." 1>&2; exit 1; fi

build:
	docker build -t howoldis .

run: build
	docker run -d --name howoldis -p 80:80  howoldis

style:
	flake8 --max-line-length=120 --statistics pypi_portal

lint:
	pylint --max-line-length=120 pypi_portal

test:
	python -m unittest tests.test_app

testpdb:
	py.test --pdb tests

update_translation:
	pybabel update -i app/messages.pot -d app/translations

etract_translation:
	pybabel extract -F app/babel.cfg -o app/messages.pot app/

translation:
	# compile translation
	pybabel compile -d app/translations

testcovweb:
	py.test --cov-report html --cov pypi_portal tests
	open htmlcov/index.html

pipinstall: isvirtualenv
	# For development environments. Symlinks are for PyCharm inspections to work with Flask-Statics-Helper.
	pip install -r requirements.txt flake8 pylint ipython pytest-cov
	[ -h pypi_portal/templates/flask_statics_helper ] || ln -s `python -c "$(PYCODE)"`/templates/flask_statics_helper \
		pypi_portal/templates/flask_statics_helper
	[ -h pypi_portal/static/flask_statics_helper ] || ln -s `python -c "$(PYCODE)"`/static \
		pypi_portal/static/flask_statics_helper
