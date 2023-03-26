from dotenv import load_dotenv
import os


load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')
DB_PATH = os.environ.get('DB_PATH')
