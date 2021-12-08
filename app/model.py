# this is the file for data table init

from app import db, app
from flask_login import UserMixin

has = db.Table('has',
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id')),
    db.Column('id', db.Integer, db.ForeignKey('user.id'))
)

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20))
    members = db.relationship('User', secondary=has, backref=db.backref('attendences', lazy='dynamic'))


class User(UserMixin, db.Model):
    # user_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    objectives = db.relationship('Objective', backref='owner')


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date = db.Column(db.Date)
    obj_per = db.Column(db.Float)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keyResults = db.relationship('KeyResult', backref='superior')

class KeyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dcp = db.Column(db.String(50))
    now = db.Column(db.Integer)
    total = db.Column(db.Integer)
    step = db.Column(db.Integer)
    kr_per = db.Column(db.Float)
    urgency = db.Column(db.String(10))
    note = db.Column(db.String(500))

    superior_id = db.Column(db.Integer, db.ForeignKey('objective.id'))
    
