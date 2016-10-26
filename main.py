from flask import Flask, make_response, flash, redirect, request
from uuid import uuid4
import urllib
import urllib2
from urlparse import urlparse
import logging
import jinja2
import os

try:
    from models import User
except ImportError as e:
    print("GAE Environment not detected")


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = Flask(__name__)
app.secret_key = 'SECRET_DUMMY'
app.debug = True
app.config['GITHUB_CLIENT_ID'] = '80cfec1f418d434c1d71'
app.config['GITHUB_CLIENT_SECRET'] = '71b3b3a810a6ba696f6b2bdedacee67aa4971676'
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'


@app.route('/')
def main():
    template = JINJA_ENVIRONMENT.get_template('index.html')
    secret = str(uuid4())
    return template.render(secret=secret)

@app.route('/login')
def login():
    url = 'https://github.com/login/oauth/authorize'
    values = {'client_id': app.config['GITHUB_CLIENT_ID'],
              'redirect_uri': 'http://dateaproject.appspot.com/github-callback',
              'state': str(uuid4())}
    try:
        data = urllib.urlencode(values)
    except:
        data = urllib.parse.urlencode(values)
        
    return redirect('?'.join([url, data]))
    
@app.route('/github-callback')
def authorized():
    url = 'https://github.com/login/oauth/access_token'
    next_url = '/dashboard'

    oauth_token = request.args.get('code')
    
    if not oauth_token:
        access_token = requests.args.get('access_token')
        if access_token:
            return redirect('/dashboard')
        else:
            flash("Authorization failed")
            return redirect('/')

    user = User.query_access(oauth_token)
    if not user:
        user = User(access_token=oauth_token)
        user.put()

    values = {'client_id': app.config['GITHUB_CLIENT_ID'],
              'client_secret': app.config['GITHUB_CLIENT_SECRET'],
              'code': oauth_token,
              'redirect_uri': 'http://dateaproject.appspot.com/github-callback',
              'state': str(uuid4())}

    try:
        data = urllib.urlencode(values)
    except:
        data = urllib.parse.urlencode(values)
        
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    rep_data = response.read()

    parsed_response = {}
    for part in rep_data.split('&'):
        key, value = part.split('=')
        parsed_response[key] = value
 
    if 'access_token' in parsed_response:
        return redirect('/dashboard')
    else:
        flash("Authorization failed")
        return rep_data
        

@app.route('/dashboard')
def dashboard():
    template = JINJA_ENVIRONMENT.get_template('dashboard.html')
    return template.render()


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