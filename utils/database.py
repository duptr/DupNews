import sqlite3
import os

# Path of the database file (will be saved in the root directory of the project)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'news.db')

def create_db():
    # Create the database and table
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop the existing table
    cursor.execute("DROP TABLE IF EXISTS news")

    # Create a new table
    cursor.execute("""
    CREATE TABLE news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        link TEXT UNIQUE,
        summary TEXT,
        date TEXT,
        translation_title TEXT,
        translation_summary TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_news(title, link, summary, date, translation_title, translation_summary, source):
    # Save the news to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO news (title, link, summary, date, translation_title, translation_summary, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, link, summary, date, translation_title, translation_summary, source)
        )
        conn.commit()
        print(f"✔ News has been saved.: {title}")
    except sqlite3.IntegrityError:
        print(f"❗ The News has already been saved.: {title}")
    finally:
        conn.close()

def get_all_news():
    # Fetch all news from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, link, summary, date, translation_title, translation_summary, source FROM news")
    news_list = cursor.fetchall()

    conn.close()
    return news_list

# Create the database when the program runs
create_db()
