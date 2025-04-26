from api.api import app
import uvicorn

from src.db_helpers.db_helpers import load_json_into_db
from src.utils.utils import download_nobel_json, get_nobel_prizes_file_path, get_db_file_path


def main():
    download_nobel_json()
    load_json_into_db(get_nobel_prizes_file_path(), get_db_file_path())

    # Note: Using host="0.0.0.0" makes this API accessible to anyone on the same network.
    # If running locally without Docker and external access is not needed,
    # change to "127.0.0.1" to restrict access to the local machine only.
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()