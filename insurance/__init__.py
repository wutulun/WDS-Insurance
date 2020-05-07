from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd07aabd6cd1fadedcf612e2ea67b3079'   # for safety
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'    # database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from insurance import routes    # Beware of the cuicular-imports problem!