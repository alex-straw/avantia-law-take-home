import json
import sqlite3


def load_json_into_db(json_file, db_path):

    if db_path.exists():
        print(f"{db_path} already exists, skipping load")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE prizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT,
            category TEXT,
            laureate_name TEXT,
            motivation TEXT
        )
    ''')

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Insert each laureate into DB
    for prize in data['prizes']:
        year = prize.get('year')
        category = prize.get('category')
        laureates = prize.get('laureates', [])

        for laureate in laureates:
            firstname = laureate.get('firstname', '')
            surname = laureate.get('surname', '')
            name = (firstname + ' ' + surname).strip()
            motivation = laureate.get('motivation', '')

            cursor.execute('''
                INSERT INTO prizes (year, category, laureate_name, motivation)
                VALUES (?, ?, ?, ?)
            ''', (year, category, name, motivation))

    conn.commit()
    conn.close()
    print(f"{db_path} created and populated successfully")