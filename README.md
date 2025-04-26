# Avantia Law Take Home

To build the Dockerfile run this command from the project root:
```commandline
docker build -t avantia-law-take-home .
```

To run the created Dockerfile run this command:
```commandline
docker run --rm -p 8000:8000 avantia-law-take-home
```

To access the fastapi Swagger on the host computer go to:
```
http://localhost:8000/docs
```

## Poetry

To install dependencies required to run the project locally run:
```commandline
poetry install
```

To install dependencies required to run tests locally run:
```commandline
poetry install --with test
```

## Tests

Install the project dependencies (including test dependencies):

```bash
poetry install --with test
```

Then run the tests from the project root:

```bash
poetry run pytest
```