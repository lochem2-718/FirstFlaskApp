from flask import Flask, render_template
from db import Database
from api import api_controller

server = Flask(__name__.split('.')[0])
server.config['SERVER_NAME'] = 'weinberger.com'
server.url_map.default_subdomain = 'www'
server.register_blueprint( api_controller )

@server.route('/')
def index():
    db = Database()
    dummy_user = db.read_user( 'username' )
    return render_template('index.html')


if __name__ == '__main__':
    server.run()
