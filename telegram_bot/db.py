import sqlite3

import termcolor

from . import env
from . import logger

def init_db():
    db_filename = env.get_env('DATABASE', './votes.db')
    if len(db_filename) == 0:
        return None

    db_connection = sqlite3.connect(db_filename)
    with db_connection:
        db_connection.execute('''CREATE TABLE IF NOT EXISTS votes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL CHECK (action IN ('accept', 'reject')),
            UNIQUE (chat_id, message_id, user_id)
        )''')

    logger.get_logger().info(
        'connect to the database ' + termcolor.colored(db_filename, 'green'),
    )

    return db_connection
