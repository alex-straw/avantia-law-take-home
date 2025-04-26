from fastapi.testclient import TestClient
from src.api.api import app
from src.db_helpers.db_helpers import load_json_into_db
from src.utils.utils import download_nobel_json, get_nobel_prizes_file_path, get_db_file_path

client = TestClient(app)


def setup_db():
    download_nobel_json()
    load_json_into_db(get_nobel_prizes_file_path(), get_db_file_path())


def test_get_prizes():
    setup_db()

    response = client.get("/prizes")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    assert "year" in data[0]
    assert "category" in data[0]
    assert "laureate_name" in data[0]
    assert "motivation" in data[0]


def test_exact_search_specific_filter():
    setup_db()

    # Very specific query: category=PHYSICS (test for case invariance) and year=2024
    response = client.get("/exact-search?category=PHYSICS&year=2024")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Should be exactly two matches

    prize = data[0]
    assert prize["category"].lower() == "physics"
    assert prize["year"] == "2024"

    prize = data[1]
    assert prize["category"].lower() == "physics"
    assert prize["year"] == "2024"


def test_fuzzy_search_many_best_matches():
    setup_db()

    response = client.get("/fuzzy-search?query=physiC")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 227

    prize = data[0]
    assert prize["category"].lower() == "physics"
    assert prize["year"] == "2024"


def test_fuzzy_search_single_match():
    setup_db()

    response = client.get("/fuzzy-search?query=Albret Enstein")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    prize = data[0]
    assert prize["category"].lower() == "physics"
    assert prize["year"] == "1921"  # photoelectric effect


def test_fuzzy_search_empty_query_string_returns_everything():
    # This could definitely be an api exception instead, not ideal to return all the data.
    setup_db()

    response = client.get("/fuzzy-search?query=")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1012