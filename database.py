import sqlite3

DB_NAME = "toranj.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # جدول کاربران
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id INTEGER UNIQUE,

            username TEXT,

            level TEXT DEFAULT 'تعیین نشده',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # جدول آزمون تعیین سطح
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tests (

            telegram_id INTEGER PRIMARY KEY,

            current_question INTEGER DEFAULT 0,

            score INTEGER DEFAULT 0,

            is_active INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# =========================
# USERS
# =========================

def add_user(telegram_id, username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (telegram_id, username)

        VALUES (?, ?)
        """,
        (telegram_id, username)
    )

    conn.commit()
    conn.close()


def get_user(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            telegram_id,
            username,
            level,
            created_at

        FROM users

        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def update_level(telegram_id, level):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET level = ?

        WHERE telegram_id = ?
        """,
        (level, telegram_id)
    )

    conn.commit()
    conn.close()


# =========================
# TESTS
# =========================

def start_test(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO tests
        (
            telegram_id,
            current_question,
            score,
            is_active
        )

        VALUES (?, 0, 0, 1)
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def get_test_progress(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            current_question,
            score,
            is_active

        FROM tests

        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


def get_test_info(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            current_question,
            score,
            is_active

        FROM tests

        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result


def set_question(telegram_id, question_number):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tests

        SET current_question = ?

        WHERE telegram_id = ?
        """,
        (question_number, telegram_id)
    )

    conn.commit()
    conn.close()


def add_score(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tests

        SET score = score + 1

        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def finish_test(telegram_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tests

        SET is_active = 0

        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def reset_test(telegram_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tests
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    )

    conn.commit()
    conn.close()
    