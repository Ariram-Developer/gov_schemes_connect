import os
import mysql.connector
from mysql.connector import pooling
from flask import current_app, g

def get_pool():
    """Initializes the MySQL connection pool using Flask app config."""
    if 'db_pool' not in current_app.config:
        # Explicitly force port to be an integer
        port_val = current_app.config.get('DB_PORT', 3306)
        try:
            port_val = int(port_val)
        except (ValueError, TypeError):
            port_val = 3306

        current_app.config['db_pool'] = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="gov_pool",
            pool_size=5,
            pool_reset_session=True,
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_NAME'],
            port=port_val
        )
    return current_app.config['db_pool']

def get_db():
    """Fetches a connection from the pool for the current request context."""
    if 'db' not in g:
        g.db = get_pool().get_connection()
    return g.db

def close_db(e=None):
    """Returns the connection back to the pool at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Registers the close_db function to run after every request."""
    app.teardown_appcontext(close_db)