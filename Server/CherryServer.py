import os

import cherrypy


try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
try:
    import _winreg as winreg
except ImportError:
    import winreg

import Server.Config as Config
from Server import vghd
from Server.PlaylistHandler import PlaylistHandler
from Server.Ajax import AjaxHandler
from Server.ServerUtils.HtmlHelper import HTMLHelper
from Server.ServerUtils.Utils import launchAsChromeApp, launchApplication


class CherryServer(object):
    def __init__(self, absDir, ip_port):
        """ Initialize all needed modules. """
        # root directory
        self.absdir = absDir
        # the ip and port the server will serve on
        self.ipport = ip_port
        # handles common ajax related requests
        self.ajax = AjaxHandler(absDir)
        # handles playlist related requests
        self.playlist = PlaylistHandler(absDir, ip_port)
        self.html = ""
        self.loadplaylist()

    def loadplaylist(self):
        pl = self.playlist.pl
        self.html = HTMLHelper(self.absdir, self.ipport, pl.lists)
        
    @cherrypy.expose
    def index(self):
        """ The home page """
        return self.cards()

    @cherrypy.expose
    def cards(self, start=0):
        # returns all the models' cards
        # 10 on each page
        start = int(start)
        end = start + 10

        if end > len(vghd.ModelDemos):
            end = len(vghd.ModelDemos)
            start = end - 10

        # meanwhile, the playlists might have changed
        # so we need to reload them
        self.loadplaylist()

        html = self.html.init("Cards")
        models = vghd.getModels(start, end)

        html.div()
        # the pagination links
        if start > 0:
            html.a("Prev", href="/cards/{}".format(start - 10))
        if end < len(vghd.ModelDemos):
            html.a("Next", href="/cards/{}".format(end))
        html.add(" Pages: ")
        for idx in range(start - 40, start + 50, 10):
            if idx in range(0, len(vghd.ModelDemos)):
                if idx == start:
                    html.add("{} ".format(int(idx / 10) + 1))
                else:
                    html.a("{}".format(int(idx / 10) + 1), href="/cards/{}".format(idx))
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

        # display models in sorted order, or randomly as they were loaded
        if Config.models_sorted:
            keys = sorted(models)
        else:
            keys = models.keys()

        for cardno in keys:
            html.div(class_="left")
            html.a(href="/card/{}".format(cardno))
            html.img(src=r"/image/{0}/{0}c.jpg".format(cardno))
            html.a.close()
            html.br()
            html.a("Play All", href="javascript:play('{}', '0');".format(cardno))
            html.div.close()

        return "{}".format(html)

    @cherrypy.expose
    def cardspage(self, pgno, **kwargs):
        # alias for cards()
        try:
            pgno = int(pgno)
            return self.cards(pgno * 10)
        except ValueError:
            return self.cards()

    @cherrypy.expose
    def card(self, id):
        # returns info about a specific card

        if id not in vghd.ModelDirs:
            return self.cards()

        # reload the playlists
        self.loadplaylist()

        html = self.html.init("Card {}".format(id))
        html.div(class_="left")
        html.a(href="javascript:play('{}', '0');".format(id))
        html.img(src=r"/image/{0}/{0}_full.png".format(id), class_="left")
        html.a.close()
        html.div.close()

        count = len(vghd.ModelDemos[id])
        html.p("No. of Demos: {}".format(count))
        for demo in vghd.ModelDemos[id]:
            html.a(demo, href="javascript:play('{}', '{}');".format(id, demo))
            # add a link to add to the playlists
            if len(self.playlist.pl.lists) > 0:
                html.a("[+]", href="javascript:pl.AddClip('{}', '{}');".format(id, demo))
            html.br()

        # all the available info about the card
        model = vghd.ModelInfo(id)
        html.b()
        html.p(model.name())
        html.b.close()
        html.p("Outfit: {}".format(model.outfit()))
        html.p("City: {}".format(model.city()))
        html.p("Country: {}".format(model.country()))
        html.p("Description: {}".format(model.description()))
        html.p("Cards: ")

        for cardId in model.cards():
            html.add("{} ".format(cardId))

        html.p("Additional collected cards: ")
        for cardId in model.collectedCards():
            html.a(href="/card/{}".format(cardId))
            html.img(src=r"/image/{0}/{0}c.jpg".format(cardId), width="60px")
            html.a.close()
            html.add(" ")


        return "{}".format(html)

    @cherrypy.expose
    def search(self, **kwargs):
        # search models by name or id or outfit
        self.loadplaylist()
        if "name" in kwargs:
            search_term = kwargs["name"]
            html = self.html.init("Search name '{}'".format(search_term))
            models = vghd.search(name=search_term)
        elif "id" in kwargs:
            search_term = kwargs["id"]
            html = self.html.init("Search id '{}'".format(search_term))
            models = vghd.search(id=search_term)
        elif "outfit" in kwargs:
            search_term = kwargs["outfit"]
            html = self.html.init("Search outfit '{}'".format(search_term))
            models = vghd.search(outfit=search_term)
        else:
            return self.cards()

        count = len(models)
        if len(models) > 20:
            models = models[:20]
            html.p("Found {} items for '{}'. Showing only the first 20 items.".format(count, search_term))
        else:
            html.p("Found {} items for '{}'.".format(count, search_term))

        for model in models:
            html.div()
            html.a(href="/card/{}".format(model[0]))
            html.img(src=r"/image/{0}/{0}c.jpg".format(model[0]))
            html.a.close()
            html.p("{} by {} ({}) from {}, {}".format(
                model[2].title(),   # outfit
                model[1].title(),   # name
                model[0],           # id
                model[3].title(),   # city
                model[4].title()    # country
            )
            )
            html.a("Play all of {}".format(model[2].title()), href="javascript:play('{}', '0');".format(model[0]))
            html.div.close()
            html.br()

        return "{}".format(html)

    @cherrypy.expose
    def execute(self, command):
        # execute an ajax request
        return self.ajax.index(command)

    @cherrypy.expose
    def reload(self):
        # reload all the vghd models.
        # this is needed to load the newly downloaded demo by vghd
        # after the server has started
        vghd.Load()
        idxbld = vghd.index_builder()
        idxbld.start()
        return self.cards()

    @cherrypy.expose
    def help(self):
        self.loadplaylist()
        html = self.html.helpInstruction()
        return "{}".format(html)


def StartServer(absDir):

    print("PyVGDemo - Python VirtuaGirl Demo Player")
    print()

    # detect the userkey in HKEY_USERS
    for i in range(20):
        # check the first 20 subkeys, which should be more than enough
        try:
            key = winreg.EnumKey(winreg.HKEY_USERS, i)
        except WindowsError:
            # we have reached the end of the list of subkeys
            Config.regId = None
            break
        else:
            # check if vghd key exists in the current userkey
            try:
                winreg.OpenKey(winreg.HKEY_USERS, key + r"\Software\Totem\vghd", 0, winreg.KEY_ALL_ACCESS)
                Config.regId = key
            except WindowsError:
                # nope, it doesn't exist
                pass
            else:
                # yep, we found it. Load the settings
                Config.vdhd_data = vghd.dataDir()
                Config.vghd_models = vghd.modelsDir()
                Config.vdhd_exe = vghd.exePath()

                vghd.Load()
                idxbld = vghd.index_builder()
                idxbld.start()
                break

    if Config.vdhd_data is None:
        # at this point we have nothing else to do.
        # perhaps we don't support the current version of the VGHD?
        # or its not installed properly?
        raise RuntimeError("Failed to determine the VGHD settings.")

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
            },
            '/favicon.ico': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.join(absDir, "Server/Media/favicon.ico")
            },
            '/media': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(absDir, "Server/Media/")
            }
        }

    cherrypy.server.socket_host = Config.ip_port[0]
    cherrypy.server.socket_port = Config.ip_port[1]
    cherrypy.server.thread_pool = 10
    cherrypy.server.environment = "production"
    cherrypy.request.show_traceback = False

    # start the vghd, not a problem if already running
    launchApplication(Config.vdhd_exe)

    # whether to open browser specified in config.
    if Config.start_browser:
        launchAsChromeApp("http://%s:%d/" % Config.ip_port)

    try:
        urllib2.urlopen("http://%s:%d/" % Config.ip_port, timeout=15)
    except urllib2.URLError:
        cherrypy.quickstart(CherryServer(absDir, Config.ip_port), config=config)
    else:
        input("Server already running!")
