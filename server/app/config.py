import os
from dotenv import load_dotenv

# Load .env from the server directory
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'
    
    RAWG_API_KEY = os.getenv('RAWG_API_KEY', '')
    RAWG_BASE_URL = 'https://api.rawg.io/api'
    
    GBOOKS_API_KEY = os.getenv('GBOOKS_API_KEY', '')
    GBOOKS_BASE_URL = 'https://www.googleapis.com/books/v1'
    
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('1', 'true')
