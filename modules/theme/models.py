# -*- coding: utf-8 -*-
import requests
from flask import (Blueprint, current_app)

theme_model = Blueprint('theme_api', __name__, url_prefix='/api/theme')


@theme_model.route('/accounts', methods=['POST'])
def show_():
    api_url = current_app.config['ACCOUNTSTATS_API']


@theme_model.route('/edit/accounts', methods=['POST'])
def edit_():
    api_url = current_app.config['ACCOUNTSTATS_API']


@theme_model.route('/add/accounts', methods=['POST'])
def add_():
    api_url = current_app.config['ACCOUNTSTATS_API']


@theme_model.route('/delete/accounts', methods=['POST'])
def delete_():
    api_url = current_app.config['ACCOUNTSTATS_API']
