from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)

app.config['DEBUG'] = True

app.config["MONGODB_SETTINGS"] = {'DB': "howler"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from project.views import users
    app.register_blueprint(users)
    from project.views import howls
    app.register_blueprint(howls)
    from project.views import auth
    app.register_blueprint(auth)
    from project.views import pack
    app.register_blueprint(pack)

register_blueprints(app)

mail = Mail(app)
app.extensions['mail'] = mail

if __name__ == '__main__':
    app.run()
