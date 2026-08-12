import os
import mysql.connector
from mysql.connector import pooling
from flask import current_app, g

def get_pool():
    """Initializes the MySQL connection pool safely for Railway or Local."""
    if 'db_pool' not in current_app.config:
        host = os.environ.get('MYSQLHOST') or current_app.config.get('DB_HOST', 'localhost')
        user = os.environ.get('MYSQLUSER') or current_app.config.get('DB_USER', 'root')
        password = os.environ.get('MYSQLPASSWORD') or current_app.config.get('DB_PASSWORD', '')
        database = os.environ.get('MYSQLDATABASE') or current_app.config.get('DB_NAME', 'gov_scheme_connect')
        
        port_val = os.environ.get('MYSQLPORT') or current_app.config.get('DB_PORT', 3306)
        try:
            port_val = int(port_val)
        except (ValueError, TypeError):
            port_val = 3306

        current_app.config['db_pool'] = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="gov_pool",
            pool_size=5,
            pool_reset_session=True,
            host=host,
            user=user,
            password=password,
            database=database,
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