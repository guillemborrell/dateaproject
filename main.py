from uuid import uuid4
import logging
import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from flask import Flask, make_response
from flask_github import GitHub


app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = '80cfec1f418d434c1d71'
app.config['GITHUB_CLIENT_SECRET'] = '71b3b3a810a6ba696f6b2bdedacee67aa4971676'
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'

github = GitHub(app)

@app.route('/')
def main():
    template = JINJA_ENVIRONMENT.get_template('index.html')
    secret = str(uuid4())
    return template.render(secret=secret)

@app.route('/dashboard')
def dashboard():
    return github.authorize()
    #template = JINJA_ENVIRONMENT.get_template('dashboard.html')
    #return template.render()


#### Handlers for running locally with static files.

@app.route('/css/<name>')
def serve_css(name):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'css', name),'rb') as f:
            response = make_response(f.read())
            response.headers['Content-Type']= 'text/css'

    except IOError:
        response = make_response('')
        response.status = '404'

    return response

@app.route('/js/<name>')
def serve_js(name):
    with open(os.path.join(os.path.dirname(__file__), 'js', name),'rb') as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'text/js'

    return response

@app.route('/img/<name>')
def serve_img(name):
    with open(os.path.join(os.path.dirname(__file__), 'img', name), 'rb') as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'image/jpg'

    return response


@app.route('/font-awesome/<sub>/<name>')
def serve_fontawesome(sub, name):
    with open(os.path.join(os.path.dirname(__file__), 'font-awesome', sub,  name),'rb') as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'text/css'

    return response


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run()
