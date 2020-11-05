from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Myuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    yellow = db.Column(db.Integer)
    time = db.Column(db.String(30))

