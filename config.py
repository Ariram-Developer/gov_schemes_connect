import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_dev_key'
    
    # MySQL Database Config
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_dev_key'
    
    # MySQL Database Config
    DB_HOST = os.environ.get('DB_HOST') or os.environ.get('MYSQLHOST', 'localhost')
    DB_USER = os.environ.get('DB_USER') or os.environ.get('MYSQLUSER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or os.environ.get('MYSQLPASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME') or os.environ.get('MYSQLDATABASE', 'gov_scheme_connect')
    DB_PORT = os.environ.get('DB_PORT') or os.environ.get('MYSQLPORT', 3306)