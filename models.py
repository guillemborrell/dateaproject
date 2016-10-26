from google.appengine.ext import ndb

class User(ndb.Model):
    access_token = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def query_access(cls, token):
        return cls.query(cls.access_token==token).fetch(1)
