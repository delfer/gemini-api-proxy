import os
import logging
import sqlite3
from quart import Quart, request, Response, render_template, jsonify
from datetime import datetime
from key_manager import get_db_connection, get_sorted_keys, DATABASE_FILE, toggle_key_removed_status, add_new_key

# Assuming 'app' is initialized in main.py and imported here
# from main import app

# In a real application, you might pass the app instance or use a Blueprint
# For this refactoring, we'll assume 'app' is available globally or passed.
# If running web_interface.py directly, you would need to initialize Flask here.
# For now, we'll define the functions and assume they are registered with the app in main.py

def authenticate(username, password):
    """Basic authentication check against USER_KEYS."""
    # In a real application, use a secure method for username/password.
    # Here, we'll just check if the provided password is one of the USER_KEYS.
    # Assuming USER_KEYS is accessible, perhaps passed or imported from main.py
    # For now, let's assume it's imported or passed.
    # If imported, need to add 'from main import USER_KEYS'
    # Let's add the import for now, assuming USER_KEYS is in main.py
    from main import USER_KEYS
    return password in USER_KEYS

# This route needs to be registered with the Flask app instance.
# Assuming 'app' is imported or available.
# @app.route('/admin/keys', methods=['GET'])
async def manage_keys():
    """Web interface to view and manage API keys."""
    auth = request.authorization # Removed await
    if not auth or not authenticate(auth.username, auth.password):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    sort_by = request.args.get('sort_by', 'added_at')
    sort_order = request.args.get('sort_order', 'asc').lower()

    allowed_sort_columns = ['key', 'added_at', 'successful_requests', 'error_requests', 'errors_since_last_success', 'first_error_at', 'error_counter_started_at', 'removed']
    if sort_by not in allowed_sort_columns:
        sort_by = 'added_at' # Default sort

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc' # Default order

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM api_keys ORDER BY {sort_by} {sort_order}")
        keys_data = cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Error fetching data from database: {e}")
        keys_data = []
    finally:
        conn.close()

    # Render an HTML template (we'll create this next)
    return await render_template('keys_table.html', keys=keys_data, sort_by=sort_by, sort_order=sort_order)

# This template filter needs to be registered with the Flask app instance.
# Assuming 'app' is imported or available.
# @app.template_filter('format_timestamp')
def format_timestamp_filter(timestamp):
    """Jinja2 filter to format a Unix timestamp into a human-readable string."""
    if timestamp is None or timestamp == 0:
        return '-'
    try:
        # Convert to integer timestamp if it's a float
        timestamp = int(timestamp)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return '-'

# Function to register routes and filters with the app
async def toggle_key(key, action):
    """Toggles the removed status of a key."""
    auth = request.authorization # Removed await
    if not auth or not authenticate(auth.username, auth.password):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if action not in ['enable', 'disable']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400

    removed_status = 1 if action == 'disable' else 0
    success = toggle_key_removed_status(key, removed_status)

    if success:
        return jsonify({'success': True, 'message': f'Key {key} {action}d successfully'})
    else:
        return jsonify({'success': False, 'message': f'Failed to {action} key {key}'}), 400

async def add_key():
    """Adds a new key."""
    auth = request.authorization # Removed await
    if not auth or not authenticate(auth.username, auth.password):
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    data = await request.get_json()
    new_key = data.get('key')

    if not new_key:
        return jsonify({'success': False, 'message': 'Key is required'}), 400

    success = add_new_key(new_key)

    if success:
        return jsonify({'success': True, 'message': f'Key {new_key} added successfully'})
    else:
        return jsonify({'success': False, 'message': f'Key {new_key} already exists or failed to add'}), 400


def register_web_interface(app):
    app.add_url_rule('/admin/keys', 'manage_keys', manage_keys, methods=['GET'])
    app.add_url_rule('/toggle_key/<key>/<action>', 'toggle_key', toggle_key, methods=['POST'])
    app.add_url_rule('/add_key', 'add_key', add_key, methods=['POST'])
    app.template_filter('format_timestamp')(format_timestamp_filter)