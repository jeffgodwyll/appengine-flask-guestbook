from flask import Flask, render_template_string, request


MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
  </body>
</html>
"""

app = Flask(__name__)


@app.route('/')
def home():
    return render_template_string(MAIN_PAGE_HTML)


@app.route('/sign', methods=['GET', 'POST'])
def guestbook():
    return render_template_string('<html><body>You wrote:<pre>' +
                                  request.form['content'] +
                                  '</pre></body></html>')
