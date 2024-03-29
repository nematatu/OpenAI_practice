import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)
    app.json.ensure_ascii=False
    
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path,"flaskr.sqlite")
    )
    if test_config is None:
        app.config.from_pyfile("config.py",silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/",endpoint="index")

    def load_config(key):
        app.config[key]=os.environ[key]

    load_config("TW_CLI_KEY")
    load_config("TW_SCR_KEY")
    
    return app