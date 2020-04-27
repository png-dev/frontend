# -*- coding: utf-8 -*-
__author__ = 'dev.vn.png@gmail.com'

from flask import Flask
import os, imp
from extensions import (kvsession, csrf_protect)
from modules import theme

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
