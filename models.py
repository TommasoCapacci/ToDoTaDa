from flask_app import db, login_manager
from flask_login import UserMixin

from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# 'User' class to represent users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    todos = db.relationship('Todo', backref='author', lazy=True)

# 'Todo' class to represent todos with their data
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)