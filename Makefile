CODE = src
VENV = poetry run
BRANCH = $(shell git rev-parse --abbrev-ref HEAD)
VERSION = $(shell git rev-parse --short HEAD)
DATE = $(shell date +%F)

ifeq ($(IMAGE_TAG),)
	export IMAGE_TAG = $(BRANCH)-$(VERSION)-$(DATE)
endif


build-%:
	docker-compose build $(subst build-,,$@)

up-%: build-%
	docker-compose up $(subst up-,,$@)

lint:
	$(VENV) flake8 --jobs 4 --statistics $(CODE)
	$(VENV) pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV) black --target-version py38 --check --line-length 120 --skip-string-normalization $(CODE)

pretty:
	$(VENV) unify --in-place --recursive $(CODE)
	$(VENV) black  --target-version py38 --line-length 120 --skip-string-normalization $(CODE)
	$(VENV) isort --recursive $(CODE)
