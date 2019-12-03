from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from config import config_options
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from logging import FileHandler, WARNING


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
mail = Mail()
simple = SimpleMDE()


def create_app(config_name):
    '''
    '''
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Intializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)

    # Will add the views and forms

    # Registering the main application blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Registering the authentication application blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/authenticate')

    # configure UploadSet
    configure_uploads(app, photos)

    if not app.debug:
        error_logs_file = FileHandler('errorlog.txt', mode = 'a', delay = False, encoding = 'utf-8')
        error_logs_file.setLevel(WARNING)

        app.logger.addHandler(error_logs_file)

    return app