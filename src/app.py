from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from flask import Flask,url_for, request
load_dotenv()

api_ky = os.environ["OPENAI_API_KEY"]
client_id = os.environ.get("SP_CLI_KEY") 
client_secret = os.environ.get("SP_SCR_KEY")

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

client = OpenAI(api_key=api_ky)

print("hello")

app=Flask(__name__)

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
    return ("<p>test<p>")

@app.route("/urlfor")
def index():
    return 'index'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login'
    else:
        return 'show_the_login_form'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('profile', username='John Doe'))
