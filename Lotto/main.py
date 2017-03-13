#!/usr/bin/env python
import os
import jinja2
import webapp2
from random import randint

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
        return self.render_template("index.html")

class LottoHandler(BaseHandler):
    def get(self):
        lucky_numbers = create_lotto_numbers(8)
        lucky_numbers = {"numbers": lucky_numbers}
        return self.render_template("lotto.html", lucky_numbers)

def create_lotto_numbers(stevilo_stevilk):
    stevilke = []
    while True:
        if len(stevilke) == stevilo_stevilk:
            break
        nakljucna_stevilka = randint(1, 39)
        if nakljucna_stevilka not in stevilke:
            stevilke.append(nakljucna_stevilka)
            stevilke.sort()
    return stevilke

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/index.html', MainHandler),
    webapp2.Route('/lotto.html', LottoHandler),
], debug=True)
