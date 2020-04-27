# -*- coding: utf-8 -*-
from flask_script import Manager
from app import create_app, configure_app, DEFAULT_GLOBAL_CONFIG_FILE, DEFAULT_APPLICATION_CONFIG_FILE

app = create_app()
manager = Manager(app)


@manager.option('-c', '--config', dest='config_file', default=DEFAULT_APPLICATION_CONFIG_FILE)
def run_server(config_file):
    configure_app(app, filename=config_file)
    app.run(host='0.0.0.0', port=8012, use_reloader=False)


if __name__ == '__main__':
    manager.run(default_command='run_server')
