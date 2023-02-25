FROM python:3.9-bullseye

COPY src src
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml 

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir poetry==1.1.10 \
    && poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false \
    && poetry install --no-interaction --no-dev --no-ansi \
    && rm -rf /tmp/.cache/pypoetry

ENTRYPOINT [ "poetry", "run", "python", "src/run_bot.py" ]
