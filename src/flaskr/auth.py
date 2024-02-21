import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from requests_oauthlib import OAuth1Session
import urllib.parse as parse
from dotenv import load_dotenv
import os

api_key = os.environ["TW_CLI_KEY"]
api_secret = os.environ["TW_SCR_KEY"]
# Twitter Endpoint
twitter_base_url = 'https://api.twitter.com'
authorization_endpoint = twitter_base_url + '/oauth/authenticate'
request_token_endpoint = twitter_base_url + '/oauth/request_token'
token_endpoint = twitter_base_url + '/oauth/access_token'
credentials=twitter_base_url + '/1.1/account/verify_credentials.json'

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/twitter_login",methods=("GET","POST"))
def twitter_login():
    return "hello"
    # if not resp.ok:
    #     msg="Failed to fetch user info."+provider_name,
    #     flash(msg,category="error")
    #     return False
    
    # if blueprint is twitter_bp:
    #     provider_user_id=resp.json()["id_str"]
    #     provider_user_name=resp.json()["screen_name"]
    
    # select_oauth=(
    #     f"SELECT * FROM oauth WHERE"
    #     f"provider='{provider_name}' and"
    #     f"provider_user_id='{provider_user_id}'"
    # )
    # db=get_db()
    # cursor=db.cursor()
    # oauth=cursor.execute(select_oauth).fetchone()

    # if not oauth:
    #     null = type(str(), tuple(), dict(__repr__=lambda self: 'null'))()
    #     user=(null,provider_user_name,null)
    #     insert_user=f"INSERT INTO user VALUES {user}"
    #     cursor.execute(insert_user)
    #     user_id=cursor.lastrowid

    #     oauth=(null,user_id,provider_name,provider_user_id,token_string)
    #     insert_oauth=f"INSERT INTO oauth VALUES {oauth}"
    #     cursor.execute(insert_oauth)
    #     db.commit()

    #     session.clear()
    #     session['user_id']=user_id

    #     msg="Logged in successfully."+provider_name
    #     flash(msg)
    #     return False







@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username,password) VALUES (?,?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id=?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view
