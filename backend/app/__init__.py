from flask import Flask
from flask_cors import CORS
import threading


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))


app = CustomFlask(__name__)
# CORS(app)
CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Headers', 'X-custom-token'])
lock = threading.Lock()
from app import routes
