import logging
import jinja2
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from flask import Flask, make_response


app = Flask(__name__)


@app.route('/')
def main():
    template = JINJA_ENVIRONMENT.get_template('index.html')
    return template.render()

@app.route('/dashboard')
def dashboard():
    template = JINJA_ENVIRONMENT.get_template('dashboard.html')
    return template.render()


#### Handlers for running locally with static files.

@app.route('/css/<name>')
def serve_css(name):
    try:
        with open(os.path.join(os.path.dirname(__file__), 'css', name)) as f:
            response = make_response(f.read())
            response.headers['Content-Type']= 'text/css'

    except IOError:
        response = make_response('')
        response.status = '404'

    return response

@app.route('/js/<name>')
def serve_js(name):
    with open(os.path.join(os.path.dirname(__file__), 'js', name)) as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'text/js'

    return response

@app.route('/img/<name>')
def serve_img(name):
    with open(os.path.join(os.path.dirname(__file__), 'img', name)) as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'image/jpg'

    return response


@app.route('/font-awesome/<sub>/<name>')
def serve_fontawesome(sub, name):
    with open(os.path.join(os.path.dirname(__file__), 'font-awesome', sub,  name)) as f:
        response = make_response(f.read())
    
    response.headers['Content-Type'] = 'text/css'

    return response


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.run()
