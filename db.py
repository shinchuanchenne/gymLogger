import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("gym_logger.db")

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            body_part_summary TEXT,
            note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )

    cur.execute(
       """
        CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        body_part TEXT,
        order_index INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE
        );

        """        
    )


    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER NOT NULL,
            set_number INTEGER,
            weight REAL NOT NULL,
            reps INTEGER NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE
            );
        """
    )

    conn.commit()
    conn.close()

    print(f"Database initialise finished! File location: {DB_PATH.resolve()}")

if __name__ == "__main__":
    init_db()