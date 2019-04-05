# -*- encoding: utf-8 -*-
import json
import sys
import traceback

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from gevent.pywsgi import WSGIServer

from constants.server import TEMPLATE_FOLDER
from constants.server import STATIC_FOLDER

from core.exceptions import DanceWithDeathException

from core.manager import create_json_from_args
from core.manager import create_json_from_dwdexception
from core.manager import create_json_from_exception

from utils.logger import createLog
log = createLog(__name__)


app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER,
)


@app.route('/api/', methods=["GET"])
def api():
    try:
        response = create_json_from_args(request.args)
    except DanceWithDeathException as dwde:
        response = create_json_from_dwdexception(dwde)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = '    '.join(line for line in lines)
        log.error(message)
        response = create_json_from_exception(e)

    return json.dumps(response)


@app.route('/', methods=["GET"])
def home():
    return render_template(
        'home.html',
    )


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))


if __name__ == "__main__":
    
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    http_server = WSGIServer(('0.0.0.0', 12011), app)
    http_server.serve_forever()


