from google.appengine.ext import ndb

class  MovieDatabase(ndb.Model):
    naslov = ndb.StringProperty()
    ocena = ndb.IntegerProperty()
    slika = ndb.StringProperty()