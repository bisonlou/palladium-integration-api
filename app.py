import os
from api import app
from werkzeug.serving import run_simple
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('HOST')
environment = os.getenv('FLASK_ENV')

if __name__ == '__main__':
    if environment == 'production':
        run_simple(host, 8080, app, use_reloader=False)
    else:
        app.run(debug=True)
