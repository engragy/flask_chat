''' initializing and tie everything together for the app package '''

#----------------------
# app initial imports |
#----------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

#---------------------
# app configurations |
#---------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = '&?IYezU(t^Tf[n,EQ%GC9zLfL>n;80QM'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'

db = SQLAlchemy(app)
crypt = Bcrypt(app)
loginman = LoginManager(app)
loginman.login_view = 'login'
loginman.login_message_category = 'info'
socketio = SocketIO(app)

# starting the app views/routes
from flask_chat import routes