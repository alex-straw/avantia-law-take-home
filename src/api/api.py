import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.db_helpers.db_helpers import load_json_into_db
from src.utils.utils import get_db_file_path, download_nobel_json, get_nobel_prizes_file_path
import random


@asynccontextmanager
async def lifespan(_app: FastAPI):
    download_nobel_json()
    load_json_into_db(get_nobel_prizes_file_path(), get_db_file_path())
    yield


app = FastAPI(lifespan=lifespan)


def get_db_connection():
    conn = sqlite3.connect(get_db_file_path())
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/prizes")
def get_all_prizes():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prizes")
    rows = cursor.fetchall()

    results = [dict(row) for row in rows]
    return results


@app.get("/health")
async def health():
    random_n = random.random()

    if random_n < 0.1:
        return JSONResponse(content={"status": "not doing so well"}, status_code=500)

    return JSONResponse(content={"status": "ok"}, status_code=200)