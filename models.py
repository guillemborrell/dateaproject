
from google.appengine.ext import ndb

class User(ndb.Model):
    oauth_token = ndb.StringProperty()
    access_token = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    uid = ndb.IntegerProperty()
    login = ndb.StringProperty()
    avatar = ndb.StringProperty()
    company = ndb.StringProperty()
    location = ndb.StringProperty()
    bio = ndb.StringProperty()
    blog = ndb.StringProperty()
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    
    @classmethod
    def query_oauth(cls, token):
        return cls.query(cls.oauth_token==token).fetch(1)

    @classmethod
    def query_access(cls, token):
        return cls.query(cls.access_token==token).fetch(1)

    @classmethod
    def query_uid(cls, uid):
        return cls.query(cls.uid==uid).order(-cls.date).fetch(1)
