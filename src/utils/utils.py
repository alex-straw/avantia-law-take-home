from pathlib import Path

import requests


def get_nobel_prizes_file_path():
    return get_project_root() / "nobel_prizes.json"


def get_db_file_path():
    return get_project_root() / "nobel.db"


def download_nobel_json():
    save_path = get_nobel_prizes_file_path()

    if save_path.exists():
        print(f"{save_path} already exists in project root, skipping download.")
        return

    url = "https://api.nobelprize.org/v1/prize.json"

    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        raise ValueError("Failed to download nobel prize dataset")


def get_project_root():
    return Path(__file__).resolve().parent.parent.parent