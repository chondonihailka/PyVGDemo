import os
import cherrypy
try:
    import urllib2
except NameError:
    import urllib.request as urllib2

import Config
from . import vghd
from .Media import MediaHandler
from .Ajax import AjaxHandler
from .ServerUtils.HtmlHelper import HTMLHelper
from .ServerUtils.Utils import launchAsChromeApp
from .Settings import SettingsHandler

class CherryServer(object):
    def __init__(self, absDir, ip_port):
        """ Initialize all needed modules. """

        self.ajax = AjaxHandler(absDir)
        self.html = HTMLHelper(absDir, ip_port)
        self.media = MediaHandler()
        self.settings = SettingsHandler(absDir)
        self.settings.load()

    @cherrypy.expose
    def index(self):
        """ The home page """
        if not os.path.isdir(Config.vdhd_data) or not os.path.isdir(Config.vghd_models):
            return self.settings.index()
        else: return self.cards()

    @cherrypy.expose
    def cards(self, start = 0):
        start = int(start)
        end = start + 10
        if end > len(vghd.ModelDemos):
            end = len(vghd.ModelDemos)
            start = end - 10

        html = self.html.init("Cards")
        models = vghd.getModels(start, end)

        html.div()
        if start > 0:
            html.a("Prev", href="/cards/{}".format(start-10))
        if end < len(vghd.ModelDemos):
            html.a("Next", href="/cards/{}".format(end))
        html.add(" Pages: ")
        for idx in range(start-40, start+50, 10):
            if idx in range(0, len(vghd.ModelDemos)):
                if idx == start:
                    html.add("{} ".format(int(idx/10) + 1))
                else:
                    html.a("{}".format(int(idx/10) + 1), href="/cards/{}".format(idx))
                    html.add(" ")

        if end < len(vghd.ModelDemos):
            html.a("Last", href="/cards/{}".format(len(vghd.ModelDemos) - 10))

        html.form(method="get", action="/cardspage/", class_="right")
        html.add("Jump to: ")
        html.input(type="text", size="2", name="pgno", value="")
        html.input(type="submit", size="10", value="GO", onclick="gotoPage();")
        html.form.close()
        html.div.close()
        html.hr()

        for id in sorted(models):
            html.div(class_="left")
            html.a(href="/card/{}".format(id))
            html.img(src=r"/image/{0}/{0}c.jpg".format(id))
            html.a.close()
            html.br()
            html.a("Play All", href="/ajax/play/{}".format(id))
            html.div.close()

        return "{}".format(html)

    @cherrypy.expose
    def cardspage(self, pgno, **kwargs):
        try:
            pgno = int(pgno)
            return self.cards(pgno*10)
        except:
            return self.cards()

    @cherrypy.expose
    def card(self, id):
        if id not in vghd.ModelDirs:
            return self.cards()

        html = self.html.init("Card {}".format(id))
        html.div(class_="left")
        html.a(href="javascript:play('{}', '0');".format(id))
        html.img(src=r"/image/{0}/{0}_full.png".format(id), class_="left")
        html.a.close()
        html.div.close()

        count = len(vghd.ModelDemos[id])
        html.p("No. of Demos: {}".format(count))
        for demo in vghd.ModelDemos[id]:
            demoId = demo.split(".")[0].split("_")[1]
            html.a(demo, href="javascript:play('{}', '{}');".format(id, demo))
            html.br()

        model = vghd.ModelInfo(id)
        html.p("Name: {}".format(model.name()))
        html.p("City: {}".format(model.city()))
        html.p("Country: {}".format(model.country()))
        html.p("Description: {}".format(model.description()))
        html.p("Cards: ")

        for cardId in model.ids():
            html.add("{} ".format(cardId))

        html.p("Additional collected cards: ")
        for cardId in model.collectedIds():
            html.a(cardId, href="/card/{}".format(cardId))
            html.add(" ")

        return "{}".format(html)

    @cherrypy.expose
    def execute(self, command):
        return self.ajax.index(command)

    @cherrypy.expose
    def help(self):
        html = self.html.helpInstruction()
        return "{}".format(html)


def StartServer(absDir):
    config = \
    {
        '/': {
            'tools.sessions.on': True,
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8'
        },
        '/image': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': Config.vdhd_data
        }
    }

    cherrypy.server.socket_host = Config.ip_port[0]
    cherrypy.server.socket_port = Config.ip_port[1]
    cherrypy.server.thread_pool = 10
    cherrypy.server.environment = "production"
    cherrypy.request.show_traceback = False

    serv = None
    # ping to see server is already running on the current ip_port
    try:
        serv = urllib2.urlopen("http://%s:%d/" %Config.ip_port, timeout=15)
    except urllib2.URLError as err: pass

    # whether to open browser specified in config.
    if Config.start_browser:
        launchAsChromeApp("http://%s:%d/" %Config.ip_port)

    if not serv:
        cherrypy.quickstart(CherryServer(absDir, Config.ip_port), config=config)