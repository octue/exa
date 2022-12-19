FROM windpioneers/gdal-python:little-gecko-gdal-2.4.1-python-3.9-slim

# Set the application root directory (using a different base so we have to repeat this)
ENV PROJECT_ROOT=/workspace
WORKDIR $PROJECT_ROOT

# Install poetry and dependencies
ENV POETRY_HOME=/root/.poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH "$POETRY_HOME/bin:$PATH"
RUN poetry config virtualenvs.create false

# Ensure the backend modules are found by tools like pylint
ENV PYTHONPATH=${PROJECT_ROOT}/backend:${PYTHONPATH}

# Service must listen to $PORT environment variable
ENV PORT 8000

# Ensure print statements and log messages promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Install python dependencies - utilise layer caching for quick rebuilds
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Copy local code to the application root directory
COPY . .

# Already installed dependencies, now install local packages like `wq` executable
RUN poetry install

# ENTRYPOINTS AND STARTUP SCRIPTS
# ===============================

# By default, run the production web service on container startup
CMD exa serve --port $PORT
