from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    url_for,
    request,
    render_template,
    make_response,
    redirect,
    abort,
    session,
    flash,
)

load_dotenv()

api_ky = os.environ["OPENAI_API_KEY"]
client_id = os.environ.get("SP_CLI_KEY")
client_secret = os.environ.get("SP_SCR_KEY")

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id, client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = OpenAI(api_key=api_ky)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/test/int/<int:num>/")
def int(num):
    return f"your num is, {(num)}"


@app.route("/test/path/<path:path>")
def path(path):
    return f"your path is, {(path)}"


@app.route("/test/uuid/<uuid:uuid>")
def uuid(uuid):
    return f"your uuid is, {(uuid)}"


@app.route("/test/string/<string:name>")
def string(name):
    return f"Hello, {(name)}"


@app.route("/test")
def test():
    return "<p>test<p>"

@app.route("/user/<username>")
def profile(username):
    return f"{username}'s profile"


with app.test_request_context():
    print(url_for("index"))


def valid_login(username, password):
    # ユーザー名とパスワードの検証ロジックをここに書く
    pass


def log_the_user_in(username):
    # ユーザーをログインさせるロジックをここに書く
    pass


@app.route("/hello/")
def hello():
    username = None
    # if request.cookies.get("username"):
    #     username=request.cookies.get("username")
    if "username" in session:
        username = session["username"]
    return render_template("hello.html", name=username)


with app.test_request_context("/hello", method="POST"):
    assert request.path == "/hello"
    assert request.method == "POST"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        error = None
        username = request.form["username"]
        password = request.form["password"]
        if username and password:
            # response=make_response(render_template("result.html", username=username))
            # response.set_cookie("username", username)
            session["username"] = username
            flash("You were successfully logged in")
            return redirect(url_for("index"))
        else:
            return render_template("result.html", error="Invalid username/password")
    elif request.method == "GET":
        return "getだ〜"
    # return render_template('result.html',error=error)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("hello"))


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "no file part"
        f = request.files["file"]
        f.save(f.filename)
        return "upload success"


@app.route("/gotohello")
def tohello():
    return redirect(url_for("hello"))


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template("error.html"), 404)
    return resp


app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
