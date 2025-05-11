import sqlite3
import os
import time
import json

DATABASE_FILE = 'keys.db'

def initialize_db():
    """Initializes the SQLite database for storing API keys."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            added_at REAL,
            successful_requests INTEGER DEFAULT 0,
            error_requests INTEGER DEFAULT 0,
            errors_since_last_success INTEGER DEFAULT 0,
            first_error_at REAL NULL,
            error_counter_started_at REAL NULL,
            removed INTEGER DEFAULT 0 -- New flag for removal
        )
    ''')
    conn.commit()
    conn.close()

def add_keys_from_env():
    """Adds keys from the GOOGLE_KEYS environment variable to the database."""
    google_keys_str = os.environ.get('GOOGLE_KEYS')
    if not google_keys_str:
        print("GOOGLE_KEYS environment variable not set.")
        return

    keys = [key.strip() for key in google_keys_str.split('|') if key.strip()]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    added_count = 0
    for key in keys:
        try:
            cursor.execute("INSERT OR IGNORE INTO api_keys (key, added_at) VALUES (?, ?)", (key, time.time()))
            if cursor.rowcount > 0:
                added_count += 1
        except sqlite3.Error as e:
            print(f"Error adding key {key} to database: {e}")
    conn.commit()
    conn.close()
    print(f"Added {added_count} new keys from GOOGLE_KEYS.")

def remove_keys_from_env():
    """Removes keys specified in the REMOVE_GOOGLE_KEYS environment variable from the database."""
    remove_keys_str = os.environ.get('REMOVE_GOOGLE_KEYS')
    if not remove_keys_str:
        print("REMOVE_GOOGLE_KEYS environment variable not set.")
        return

    keys_to_remove = [key.strip() for key in remove_keys_str.split('|') if key.strip()]
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    removed_count = 0
    for key in keys_to_remove:
        try:
            cursor.execute("UPDATE api_keys SET removed = 1 WHERE key = ?", (key,))
            if cursor.rowcount > 0:
                removed_count += 1
        except sqlite3.Error as e:
            print(f"Error marking key {key} as removed in database: {e}")
    conn.commit()
    conn.close()
    print(f"Marked {removed_count} keys as removed specified in REMOVE_GOOGLE_KEYS.")
def get_db_connection():
    """Creates a database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def update_key_stats(key, success=True):
    """Updates statistics for a given key."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    current_time = time.time()

    try:
        if success:
            cursor.execute("""
                UPDATE api_keys
                SET successful_requests = successful_requests + 1,
                    errors_since_last_success = 0,
                    first_error_at = NULL,
                    error_counter_started_at = NULL
                WHERE key = ?
            """, (key,))
        else:
            cursor.execute("SELECT first_error_at, error_counter_started_at FROM api_keys WHERE key = ?", (key,))
            row = cursor.fetchone()
            first_error_at, error_counter_started_at = row

            if first_error_at is None:
                first_error_at = current_time
            if error_counter_started_at is None:
                error_counter_started_at = current_time

            cursor.execute("""
                UPDATE api_keys
                SET error_requests = error_requests + 1,
                    errors_since_last_success = errors_since_last_success + 1,
                    first_error_at = ?,
                    error_counter_started_at = ?
                WHERE key = ?
            """, (first_error_at, error_counter_started_at, key))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating stats for key {key}: {e}")
    finally:
        conn.close()


def get_available_keys():
    """Retrieves all keys from the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM api_keys WHERE removed = 0")
    keys = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keys

def select_best_key():
    """Selects the best key based on error count and total requests using get_sorted_keys."""
    sorted_keys = get_sorted_keys()
    if sorted_keys:
        return sorted_keys[0]
    return None

def get_sorted_keys():
    """Retrieves all keys from the database, sorted by priority."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT key FROM api_keys
        WHERE removed = 0
        ORDER BY errors_since_last_success ASC, (successful_requests + error_requests) ASC
    """)
    keys = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keys


# Initial setup
initialize_db()
add_keys_from_env()
remove_keys_from_env()

if __name__ == '__main__':
    # Example usage (for testing)
    # Set GOOGLE_KEYS and REMOVE_GOOGLE_KEYS environment variables before running
    # os.environ['GOOGLE_KEYS'] = 'key1,key2,key3'
    # os.environ['REMOVE_GOOGLE_KEYS'] = 'key2'
    # initialize_db()
    # add_keys_from_env()
    # remove_keys_from_env()

    # print("Available keys:", get_available_keys())

    # Simulate some requests
    # update_key_stats('key1', success=True)
    # update_key_stats('key1', success=False)
    # update_key_stats('key3', success=True)
    # update_key_stats('key1', success=False)

    # print("Best key:", select_best_key())
    pass