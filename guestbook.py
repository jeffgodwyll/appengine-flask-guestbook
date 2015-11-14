import cgi
import urllib

from google.appengine.api import users
# [START import_ndb]
from google.appengine.ext import ndb
# [END import_ndb]

from flask import Flask, render_template_string, request, redirect


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

app = Flask(__name__)


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]
@app.route('/')
def home():
    if request.args.get('guestbook_name'):
        guestbook_name = request.args.get('guestbook_name')
    else:
        guestbook_name = DEFAULT_GUESTBOOK_NAME

    html = render_template_string('<html><body>')

    # Ancestor Queries, as shown here, are strongly consistent
    # with the High Replication Datastore. Queries that span
    # entity groups are eventually consistent. If we omitted the
    # ancestor from this query there would be a slight chance that
    # Greeting that had just been written would not show up in a
    # query.
    # [START query]
    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)
    # [END query]

    user = users.get_current_user()
    for greeting in greetings:
        if greeting.author:
            author = greeting.author.email
            if user and user.user_id() == greeting.author.identity:
                author += ' (You)'
            html = render_template_string(html + '<b>%s</b> wrote:' % author)

        else:
            html = render_template_string(html + 'An anonymous person wrote:')
        html = render_template_string(html + '<blockquote>%s</blockquote>' %
                                      cgi.escape(greeting.content))

    if user:
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
    else:
        url = users.create_login_url('/')
        url_linktext = 'Login'

    # Write the submission form and the footer of the page
    sign_query_params = urllib.urlencode({'guestbook_name':
                                          guestbook_name})
    html = render_template_string(
        html + (MAIN_PAGE_FOOTER_TEMPLATE %
                (sign_query_params, cgi.escape(guestbook_name),
                 url, url_linktext)))
    return html
# [END main_page]


# [START guestbook]
@app.route('/sign', methods=['POST'])
def guestbook():
    if request.args.get('guestbook_name'):
        guestbook_name = request.args.get('guestbook_name')
    else:
        guestbook_name = DEFAULT_GUESTBOOK_NAME

        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
        greeting.author = Author(
            identity=users.get_current_user().user_id(),
            email=users.get_current_user().email())

    greeting.content = request.form['content']
    greeting.put()

    query_params = {'guestbook_name': guestbook_name}
    return redirect('/?' + urllib.urlencode(query_params))
