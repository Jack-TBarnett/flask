import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the create_app
    app = Flask(__name__, instance_relative_config=True)# creates Flask isntance
    app.config.from_mapping(# sets default configurations
    SECRET_KEY='dev',# secures data
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),#This is where the db is saved
    )

    if test_config is None:
        #Laod the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)# overrides default config in instnace.
    else:
        #If passed in load test config
        app.config.from_mapping(test_config)

    #make sure the isntance folder is there
    try:
        os.makedirs(app.instance_path)# ensures app.instance_path exists.
    except OSError:
        pass

    #returns the page
    @app.route('/hello')
    def hello():
        return 'In the beggining'

    from . import db
    db.init_app(app)

    # apply Blueprint
    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
