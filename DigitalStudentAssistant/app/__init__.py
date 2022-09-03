from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask import session

app = Flask(__name__)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app.projects import projects as projects_bp
app.register_blueprint(projects_bp, url_prefix='/projects')


from app import routes, models, errors
