# -*- coding: utf-8 -*-
from simplekv.memory import DictStore
from flask_kvsession import KVSessionExtension
from flask_wtf.csrf import CsrfProtect
from flask import abort

store = DictStore()
kvsession = KVSessionExtension(store)
csrf_protect = CsrfProtect()


@csrf_protect.error_handler
def csrf_error(reason):
    return abort(400, {'code': 400, 'message': 'Request token missing or exprired. Please press F5 to refresh'})
