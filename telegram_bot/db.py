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

def add_vote(db_connection, chat_id, message_id, user_id, action):
    changeable_vote = env.get_env('CHANGEABLE_VOTE', 'TRUE') == 'TRUE'
    command = 'REPLACE' if changeable_vote else 'INSERT'
    with db_connection:
        db_connection.execute(
            command + ''' INTO votes(chat_id, message_id, user_id, action)
                VALUES (?, ?, ?, ?)''',
            (chat_id, message_id, user_id, action),
        )

def count_votes(db_connection, chat_id, message_id, action):
    (counter,) = db_connection.execute('''
        SELECT COUNT(*)
        FROM votes
        WHERE chat_id = ? AND message_id = ? AND action = ?
    ''', (chat_id, message_id, action)).fetchone()
    return counter
