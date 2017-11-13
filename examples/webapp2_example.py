from webapp2 import Route, WSGIApplication

APP = WSGIApplication([
    Route('/pyinfo', handler='pyinfo.wsgi.application')
])
