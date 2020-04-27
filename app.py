# -*- coding: utf-8 -*-
__author__ = 'dev.vn.png@gmail.com'

from flask import (Flask, jsonify, render_template)
import os, imp

from werkzeug.exceptions import UnsupportedMediaType

from extensions import (kvsession, csrf_protect)
from modules import theme
import logging
from logging.handlers import RotatingFileHandler
import sys
from flask_wtf.csrf import generate_csrf

DEFAULT_GLOBAL_CONFIG_FILE = '/home/sf/soc/conf/sirc.py'
DEFAULT_APPLICATION_CONFIG_FILE = 'config.py'


def load_module(filename):
    """

    :param filename:
    :return:
    """
    mod = imp.new_module('config')
    mod.__file__ = filename
    try:
        with open(filename) as config_file:
            exec(compile(config_file.read(), filename, 'exec'), mod.__dict__)
    except Exception as ex:
        raise ex
    return mod


def configure_extensions(app):
    """

    :param app:
    :return:
    """
    kvsession.init_app(app)
    csrf_protect.init_app(app)


def configure_blueprints(app):
    """

    :param app:
    :return:
    """
    app.register_blueprint(theme.theme_ctrl)
    app.register_blueprint(theme.theme_model)


def configure_log_handlers(app):
    """

    :param app:
    :return:
    """
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
    info_log = os.path.join(app.config['LOG_FOLDER'], app.config['INFO_LOG'])
    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(app.config['LOG_FOLDER'], app.config['ERROR_LOG'])
    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log,
        maxBytes=100000,
        backupCount=10
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

    handler_console = logging.StreamHandler(stream=sys.stdout)
    handler_console.setFormatter(formatter)
    handler_console.setLevel(logging.INFO)
    app.logger.addHandler(handler_console)

    app.logger.setLevel(logging.DEBUG if app.debug else logging.ERROR)

    for h in app.logger.handlers:
        h.setFormatter(formatter)


def configure_hook(app):
    """

    :param app:
    :return:
    """

    @app.after_request
    def set_csrf_cookie(response):
        response.set_cookie('X-XSRFToken', generate_csrf())
        return response


def configure_error_handlers(app):
    """

    :param app:
    :return:
    """

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.error(error, exc_info=error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 400
        else:
            return jsonify(error={'code': 400, 'message': 'Bad request'}), 400

    @app.errorhandler(401)
    def unauthorized_request(error):
        app.logger.error(error, exc_info=error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 401
        else:
            return jsonify(error={'code': 401, 'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('')

    @app.errorhandler(405)
    def request_not_found(error):
        app.logger.error(error, exc_info=error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 405
        else:
            return jsonify(error={'code': 405, 'message': 'This method is not allowed for the requested url.'}), 405

    @app.errorhandler(415)
    def request_not_support_type(error):
        app.logger.error(error, exc_info=error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 415
        else:
            return jsonify(
                error={'code': 415,
                       'message': 'The server does not support the media type transmitted in the request'}), 415

    @app.errorhandler(UnsupportedMediaType)
    def request_not_support_type_by_exception(error):
        app.logger.error(error, exc_info=error)
        if type(error.description) == dict:
            return jsonify(error=error.description), 415
        else:
            return jsonify(
                error={'code': 415,
                       'message': 'The server does not support the media type transmitted in the request'}), 415

    @app.errorhandler(Exception)
    def default_exception(error):
        app.logger.error(error, exc_info=error)
        if error.message != '':
            return jsonify(error={'code': 500, 'message': error.message}), 500
        else:
            return jsonify(error={'code': 500, 'message': 'Internal error'}), 500


def configure_main_route(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/header')
    def header():
        return render_template('header.html')


def configure_app(app, filename=DEFAULT_GLOBAL_CONFIG_FILE):
    """
    Config a flask app
    :param app:
    :param filename:
    :return: flask_app
    """
    if not os.path.isfile(filename):
        filename = DEFAULT_APPLICATION_CONFIG_FILE
    config = load_module(filename)
    app.config.from_object(config.FrontendConfig)
    # Correct LOG_FOLDER  config
    app.config['LOG_FOLDER'] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'logs'
    )
    config.make_dir(app.config['LOG_FOLDER'])

    configure_extensions(app)
    configure_blueprints(app)
    configure_log_handlers(app)
    configure_hook(app)
    configure_error_handlers(app)
    configure_main_route(app)


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(
        dict(
            variable_start_string='[[',
            variable_end_string=']]'
        )
    )


def create_app(config=None):
    """
    Create a flask app
    :param config:
    :return: flask app
    """

    app = CustomFlask(__name__)
    app.debug = True
    return app
