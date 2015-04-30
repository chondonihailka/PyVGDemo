import cherrypy

from .Static.css import css_default as css
from .Static.jquery import jq_210 as jquery
from .Static.js import js_default as js
from .Static.js import cherryjs, settingsjs
from .Static.css import css_vghd

class MediaHandler(object):
    @cherrypy.expose
    def css(self):
        cherrypy.response.headers['Content-Type'] = 'text/css'
        return css.encode('utf-8')

    @cherrypy.expose
    def jquery(self):
        cherrypy.response.headers['Content-Type'] = 'application/javascript'
        return jquery.encode('utf-8')

    @cherrypy.expose
    def js(self):
        cherrypy.response.headers['Content-Type'] = 'application/javascript'
        return js.encode('utf-8')

    @cherrypy.expose
    def cherryjs(self):
        cherrypy.response.headers['Content-Type'] = 'application/javascript'
        return cherryjs.encode('utf-8')

    @cherrypy.expose
    def vghdcss(self):
        cherrypy.response.headers['Content-Type'] = 'text/css'
        return css_vghd.encode('utf-8')

    @cherrypy.expose
    def settingsjs(self):
        cherrypy.response.headers['Content-Type'] = 'application/javascript'
        return settingsjs.encode('utf-8')
