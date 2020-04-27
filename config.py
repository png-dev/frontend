# -*- coding: utf-8 -*-
import os


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as ex:
        raise ex


class DefaultConfig(object):
    DEBUG = True

    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"
    LOG_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')


class FrontendConfig(DefaultConfig):
    """
     Config for frontend
    """
