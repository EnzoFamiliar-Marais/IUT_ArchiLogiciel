from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os.path

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p
        )
    )


app = Flask(__name__)
cors = CORS(app, resources={r"/quiz/api/v1.0/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + mkpath('../myapp.db')
)
db = SQLAlchemy(app)

