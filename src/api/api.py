import sqlite3
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from rapidfuzz import fuzz

from src.db_helpers.db_helpers import load_json_into_db
from src.utils.utils import get_db_file_path, download_nobel_json, get_nobel_prizes_file_path
import random


SEARCH_FIELDS = ["year", "category", "laureate_name", "motivation"]


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
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prizes")
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
    finally:
        conn.close()
    return results


@app.get("/exact-search")
def exact_search(
    name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    motivation: Optional[str] = Query(None),
    year: Optional[str] = Query(None)
):
    conn = get_db_connection()

    # Push down the predicates here.
    # Search for exact (case invariant) matches.
    # All fields are strings for ease (this isn't necessarily the best choice for fields like year)

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM prizes WHERE 1=1"
        params = []

        if name:
            query += " AND LOWER(laureate_name) = ?"
            params.append(name.lower())
        if category:
            query += " AND LOWER(category) = ?"
            params.append(category.lower())
        if motivation:
            query += " AND LOWER(motivation) = ?"
            params.append(motivation.lower())
        if year:
            query += " AND LOWER(year) = ?"
            params.append(year.lower())

        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        return results
    finally:
        conn.close()


@app.get("/fuzzy-search")
def fuzzy_search(
    query: str = Query(..., description="Fuzzy text search across year, category, laureate_name, and motivation")
):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prizes")
        prizes = [dict(row) for row in cursor.fetchall()]

        if not query:
            return prizes  # Return everything if no query

        scored_prizes = []
        best_score = -1

        # We consider each prize row separately
        # 1. Iterate over prizes
        # 2. Iterate over fields for each prize
        # 3. Get the highest match for the search string
        # 4. Store the prize row and its corresponding highest fuzzy match score
        # 5. Return the top matches - if you search 'PhsYcs' it should return all physics prizes rows (unless there is a better match)

        for prize_row in prizes:
            best_field_score = 0
            for field in SEARCH_FIELDS:
                value = prize_row.get(field)
                if value:
                    score = fuzz.WRatio(query, str(value))
                    best_field_score = max(best_field_score, score)

            scored_prizes.append({"prize": prize_row, "score": best_field_score})
            best_score = max(best_score, best_field_score)

        # Now select all prizes with score == best_score
        top_matches = [match["prize"] for match in scored_prizes if match["score"] == best_score]

        return top_matches
    finally:
        conn.close()


@app.get("/health")
async def health():
    random_n = random.random()

    if random_n < 0.1:
        return JSONResponse(content={"status": "not doing so well"}, status_code=500)

    return JSONResponse(content={"status": "ok"}, status_code=200)