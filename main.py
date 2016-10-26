from flask import Flask, make_response, flash, redirect, request
from uuid import uuid4
import urllib
import urllib2
from urlparse import urlparse
import logging
import jinja2
import os
import config
import json

try:
    from models import User
except ImportError as e:
    print("GAE Environment not detected")


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET
app.config['GITHUB_CLIENT_ID'] = config.GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = config.GITHUB_CLIENT_SECRET
app.config['GITHUB_BASE_URL'] = config.GITHUB_BASE_URL
app.config['GITHUB_AUTH_URL'] = config.GITHUB_AUTH_URL


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
    state = request.args.get('state')
    
    if not oauth_token:
        access_token = requests.args.get('access_token')
        if access_token:
            return redirect('/dashboard')
        else:
            flash("Authorization failed")
            return redirect('/')

    user = User.query_oauth(oauth_token)
    if not user:
        user = User(oauth_token=oauth_token)
        user.put()

    values = {'client_id': app.config['GITHUB_CLIENT_ID'],
              'client_secret': app.config['GITHUB_CLIENT_SECRET'],
              'code': oauth_token,
              'redirect_uri': 'http://dateaproject.appspot.com/github-callback',
              'state': state}

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
        try:
            response = urllib2.urlopen(
                'https://api.github.com/user?access_token={}'.format(
                    parsed_response['access_token'])
                )
            rep_data = response.read()
            user_data = json.loads(rep_data)

            user = User.query_oauth(oauth_token)[0]
            user.oauth_token=user.oauth_token
            user.access_token=parsed_response['access_token']
            user.uid=user_data['id']
            user.login=user_data['login']
            user.avatar=user_data['avatar_url']
            user.company=user_data['company']
            user.blog=user_data['blog']
            user.bio=user_data['bio']
            user.email=user_data['email']
            user.location=user_data['location']
            user.name=user_data['name']
            user.put()
            
            return redirect('/dashboard?id={}'.format(user_data['id']))
        except urllib2.HTTPError as e:
            logging.critical(parsed_response)
            return 'Internal server error. We are working on authentication now'
        
    else:
        flash("Authorization failed")
        return redirect('/')
        

@app.route('/dashboard')
def dashboard():
    uid = request.args.get('id')
    if uid:
        user = User.query_uid(int(uid))
        if user:
            user = user[0]
        else:
            user = None
    template = JINJA_ENVIRONMENT.get_template('dashboard.html')
    return template.render({'user': user})


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
