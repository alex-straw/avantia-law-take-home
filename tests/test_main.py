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