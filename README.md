# Fast API Docker Practice

This application was built using FastAPI and Docker.
Please use the Swagger page to interact with the API (see below).

## Running the Application

To build the Dockerfile run this command from the project root:
```commandline
docker build -t fast-api-docker-practice .
```

To run the created Dockerfile run this command:
```commandline
docker run --rm -p 8000:8000 fast-api-docker-practice
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

## APIs

### "/prizes"
This API endpoint returns all prizes in the table.

### "/exact-search"
This API endpoint lets you search for exact (case invariant) matches on all fields.

### "/fuzzy-search"
This API endpoint allows you to fuzzy search the data for a string.

An empty string returns all records.

For each prize row its fields are checked against the query string and the best match found.

At the end, the prize(s) with the highest score (and any with the same score) are returned.

## Further Work
1. Tidy up the API endpoint names and descriptions.
2. Provide an optional parameter to the fuzzy-search to return all other laureates associated with a prize if a fuzzy match is found.
3. Add additional test cases - e.g., testing that connections are closed properly.
4. Hardening the Dockerfile by removing unnecessary dependencies and potentially using a non-root user.
5. Add an endpoint to add/amend records.
