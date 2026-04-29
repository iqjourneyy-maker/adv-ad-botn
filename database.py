import sqlite3

# Connect database
conn = sqlite3.connect(
    "sessions.db",
    check_same_thread=False
)

cursor = conn.cursor()

################################
# USERS TABLE
################################

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    session TEXT,
    message TEXT,
    media TEXT,
    schedule INTEGER
)
""")

################################
# LOGS TABLE
################################

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total INTEGER,
    sent INTEGER,
    failed INTEGER,
    start_time TEXT,
    end_time TEXT
)
""")

conn.commit()

################################
# SAVE SESSION
################################

def save_session(user_id, session):

    cursor.execute(

        "REPLACE INTO users VALUES (?, ?, ?, ?, ?)",

        (user_id, session, None, None, None)

    )

    conn.commit()


################################
# SAVE MESSAGE
################################

def save_message(user_id, message):

    cursor.execute(

        "UPDATE users SET message=? WHERE user_id=?",

        (message, user_id)

    )

    conn.commit()


################################
# SAVE MEDIA
################################

def save_media(user_id, media):

    cursor.execute(

        "UPDATE users SET media=? WHERE user_id=?",

        (media, user_id)

    )

    conn.commit()


################################
# SAVE SCHEDULE
################################

def save_schedule(user_id, minutes):

    cursor.execute(

        "UPDATE users SET schedule=? WHERE user_id=?",

        (minutes, user_id)

    )

    conn.commit()


################################
# GET USER DATA
################################

def get_user_data(user_id):

    cursor.execute(

        "SELECT session, message, media FROM users WHERE user_id=?",

        (user_id,)

    )

    return cursor.fetchone()


################################
# REMOVE ACCOUNT
################################

def remove_account(user_id):

    cursor.execute(

        "DELETE FROM users WHERE user_id=?",

        (user_id,)

    )

    conn.commit()


################################
# GET ALL USERS
################################

def get_all_users():

    cursor.execute(
        "SELECT user_id FROM users"
    )

    return cursor.fetchall()


################################
# SAVE LOG
################################

def save_log(
    user_id,
    total,
    sent,
    failed,
    start_time,
    end_time
):

    cursor.execute(

        """
        INSERT INTO logs
        (user_id, total, sent, failed, start_time, end_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (
            user_id,
            total,
            sent,
            failed,
            start_time,
            end_time
        )

    )

    conn.commit()


################################
# GET LOGS
################################

def get_logs(user_id):

    cursor.execute(

        """
        SELECT total, sent, failed,
        start_time, end_time
        FROM logs
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 5
        """,

        (user_id,)

    )

    return cursor.fetchall()