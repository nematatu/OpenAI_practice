from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from flask import Flask, url_for, request, render_template

load_dotenv()

api_ky = os.environ["OPENAI_API_KEY"]
client_id = os.environ.get("SP_CLI_KEY")
client_secret = os.environ.get("SP_SCR_KEY")

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id, client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = OpenAI(api_key=api_ky)

print("hello")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!<p>"


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


@app.route("/urlfor")
def index():
    return "index"


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
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)


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
            return render_template("result.html", error=error, username=username)
        else:
            return render_template("result.html", error="Invalid username/password")
    elif request.method == "GET":
        return "getだ〜"
    # return render_template('result.html',error=error)

@app.route("/upload",methods=["GET","POST"])
def upload_file():
    if request.method=="POST":
        if 'file' not in request.files:
            return "no file part"
        f=request.files["file"]
        f.save(f.filename)
        return "upload success"