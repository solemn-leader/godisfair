CODE = src
VENV = poetry run

lint:
	$(VENV) flake8 --jobs 4 --statistics $(CODE)
	$(VENV) pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV) black --target-version py38 --check --line-length 120 --skip-string-normalization $(CODE)
	# $(VENV) mypy $(CODE)

pretty:
	$(VENV) unify --in-place --recursive $(CODE)
	$(VENV) black  --target-version py38 --line-length 120 --skip-string-normalization $(CODE)
	$(VENV) isort --recursive $(CODE)
