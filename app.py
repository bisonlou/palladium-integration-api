
from api import app
from os import environ
from werkzeug.serving import run_simple


host = environ['HOST']

if __name__ == "__main__":
    run_simple(host, 8080, app, use_reloader=False)
