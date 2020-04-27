# -*- coding:utf-8 -*-

from flask import (Blueprint, render_template)

theme_ctrl = Blueprint('theme', __name__, url_prefix='/theme', template_folder='views')


@theme_ctrl.route('/table')
def table_():
    """

    :return:
    """
    return render_template('index.html')


@theme_ctrl.route('/detail')
def table_detail():
    """

    :return:
    """
    return render_template('index.html')


@theme_ctrl.route('/edit')
def table_edit():
    """

    :return:
    """
    return render_template("index.html")


@theme_ctrl.route('/add')
def table_add():
    """

    :return:
    """
    return render_template('add.html')
