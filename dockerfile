# Python
FROM python:3.9

# Define env variables
ENV POETRY_VERSION=1.2.2
ENV PORT=8080
ENV SCOPE=$SCOPE

# install poetry
RUN pip install "poetry==$POETRY_VERSION"

# copy project requirement files here to ensure they will be cached.
WORKDIR /root
ADD app/ app/
ADD logs/ logs/
COPY docker/entrypoint.sh poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
ENV POETRY_VIRTUALENVS_IN_PROJECT true
RUN poetry install

EXPOSE $PORT

# Use heroku entrypoint
# CMD poetry run uvicorn "app.main:app" --host 0.0.0.0 --port 5000
CMD ["bash", "entrypoint.sh"]
