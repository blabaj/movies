#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import MovieDatabase
import time

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        vnosi = MovieDatabase.query().fetch()
        params = {"vnosi":vnosi}
        return self.render_template("movies.html", params)
    def post(self):
        naslov = self.request.get("naslov")
        if (len(naslov) == 0 or len(naslov.strip(' ')) == 0):
            napaka = {"napaka":"Naslov je potreben!"}
            return self.render_template("movies.html", napaka)

        ocena = int(self.request.get("ocena"))

        slika = self.request.get("slika")
        vnos = MovieDatabase(naslov=naslov,ocena=ocena , slika=slika)
        vnos.put()
        #pridobivanje vseh vnosov
        vnosi = MovieDatabase.query().fetch()
        params = {"vnosi":vnosi}
        return self.render_template("movies.html", params)





app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name = "seznam-vnosov"),

], debug=True)
