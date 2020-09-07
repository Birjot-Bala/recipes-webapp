import os

from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'recipes_webapp.sqlite')
    )

    # This section is needed for url_for("foo", _external=True) to automatically
    # generate http scheme when this sample is running on localhost,
    # and to generate https scheme when it is deployed behind reversed proxy.
    # See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        # test config
        app.config.update(test_config)

    Session(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    with app.app_context():
        from recipes_webapp import oauth, db, recipes

    app.register_blueprint(oauth.bp)
    app.register_blueprint(recipes.bp)

    return app
