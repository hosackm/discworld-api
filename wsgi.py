from discworld import create_app
from dotenv import load_dotenv

load_dotenv()
wsgi_app = create_app()
