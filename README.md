# Flask-Guestbook

Flask-Guestbook is an example application showing basic usage of Google App
Engine. It's mainly based on the design decisions implemented in
[Appengine Guestbook][8] but with with a touch of flask goodies thrown in :).
Users can read & write text messages and optionally log-in with their Google
account. Messages are stored in App Engine (NoSQL) High Replication Datastore
(HRD) and retrieved using a strongly consistent(ancestor) query.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [NDB Datastore API][3]
- [Users API][4]

## Dependencies
- [flask][5]
- [jinja2][6]
- [Twitter Bootstrap][7]

[1]: https://developers.google.com/appengine
[2]: https://python.org
[3]: https://developers.google.com/appengine/docs/python/ndb/
[4]: https://developers.google.com/appengine/docs/python/users/
[5]: http://flask.pocoo.org/docs/
[6]: http://jinja.pocoo.org/docs/
[7]: http://twitter.github.com/bootstrap/
[8]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python
[9]: https://github.com/GoogleCloudPlatform/appengine-flask-skeleton
