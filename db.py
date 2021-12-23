from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    db.init_app(app)


db = SQLAlchemy()
