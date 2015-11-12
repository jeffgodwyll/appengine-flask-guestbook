from google.appengine.api import users

from flask import Flask, redirect


app = Flask(__name__)


@app.route('/')
def home():
    # [START get_current_user]
    # Checks for active Google account session
    user = users.get_current_user()
    # [END get_current_user]

    # [START if_user]
    if user:
        resp = 'Hello, ' + user.nickname()
    # [END if_user]
    # [START if_not_user]
    else:
        return redirect(users.create_login_url('/'))
    # [END if_not_user]
    return resp, 200, {'content-type': 'text/html; charset=utf-8'}
