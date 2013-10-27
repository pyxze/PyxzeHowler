import datetime
from flask import url_for
from project import db
from mongoengine import *
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

    name = db.StringField(max_length=255)
    username = db.StringField(max_length=255)
    howls = ListField(ReferenceField('Howl'))

    def __unicode__(self):
        return self.email

class Pack(db.Document):
    user = ReferenceField(User)
    howlers = ListField(ReferenceField('User'))

    meta = {
        'indexes': ['user']
    }

class Howl(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    howl = db.StringField(max_length=140, required=True)
    user = ReferenceField(User)

    def __unicode__(self):
        return self.howl

    meta = {
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }
