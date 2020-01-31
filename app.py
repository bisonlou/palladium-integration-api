import os
from api import app
from werkzeug.serving import run_simple
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("HOST")


if __name__ == "__main__":
    run_simple(host, 8080, app, use_reloader=False)
