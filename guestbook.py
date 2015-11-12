import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

from flask import Flask, render_template, request, redirect, url_for


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


app = Flask(__name__)

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.args.get('guestbook_name'):
        guestbook_name = request.args.get('guestbook_name')
    else:
        guestbook_name = DEFAULT_GUESTBOOK_NAME

    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    user = users.get_current_user()
    if user:
        url = users.create_logout_url(url_for('home'))
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(url_for('home'))
        url_linktext = 'Login'

    return render_template(
        'index.html',
        user=user, greetings=greetings,
        guestbook_name=urllib.quote_plus(guestbook_name),
        url=url, url_linktext=url_linktext)


@app.route('/sign', methods=['POST'])
def sign():

    # We set the same parent key on the 'Greeting' to ensure each
    # Greeting is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second.
    if request.args.get('guestbook_name'):
        guestbook_name = request.args.get('guestbook_name')
    else:
        guestbook_name = DEFAULT_GUESTBOOK_NAME
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
        greeting.author = Author(
            identity=users.get_current_user().user_id(),
            email=users.get_current_user().email())

    greeting.content = request.form['content']
    greeting.put()

    query_params = {'guestbook_name': guestbook_name}
    return redirect(url_for('home') + '?' + urllib.urlencode(query_params))
