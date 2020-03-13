import os
from api import app
from werkzeug.serving import run_simple

host = os.environ.get('HOST')
environment = os.environ.get('FLASK_ENV')

if __name__ == '__main__':
    if environment == 'production':
        run_simple(host, 8080, app, use_reloader=False)
    else:
        app.run(host='127.0.0.1', port=8080, debug=True)