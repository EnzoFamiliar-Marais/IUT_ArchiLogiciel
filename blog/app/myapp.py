from flask import Flask
app = Flask (__name__)

from .extensions import api, db
from .views import ns

# initialisation de la BD
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

# initialisation de restx
api.init_app(app)
db.init_app(app)
api.add_namespace(ns)
