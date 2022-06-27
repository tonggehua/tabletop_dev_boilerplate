from flask import Flask, abort, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from os import environ # this line should go at the top of your file

app = Flask(__name__)
app.config["SECRET_KEY"] = "never-tell-anyone-how-I-spin"
app.config["TESTING"] = False

# App - connect to other libraries to enable stuff
# 1. Enable database through SQLAlchemy
# Add database location
#app.config['SQLALCHEMY_DATABASE_URI'] = 'splite:///myDB.db'
### -> uses DATABASE_URL (connecting to PostgreSQL instead of SQLite IF POSSIBLE, for Heroku deployment)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///biobusDB.db'
# Turn off notification at every change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Create database and bind it to app
db = SQLAlchemy(app)

# 2. Enable Authentication through flask_login
# Login manager
login_manager = LoginManager()
login_manager.init_app(app)


# 3. Database checks
# Check that database exists and contains the admin entry
# If not, initialize database & add admin entry






if __name__ == '__main__':
    import routes
    app.run()