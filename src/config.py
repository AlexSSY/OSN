from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')
DB_PATH = os.environ.get('DB_PATH')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
