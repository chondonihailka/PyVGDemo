import cherrypy

from .ServerUtils.ConfigPHelper import Configuration
from .ServerUtils import Markup
from . import vghd


class AjaxHandler(object):
    def __init__(self, absDir):
        self.absDir = absDir
        self.cfg = Configuration(self.absDir)
        self.crawlerRunning = False
        self.listPlayer = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, command):
        """
        @param command: ajax request
        @return: json formatted html
        """
        if command.startswith("/"):
            if command == "/shutdown":
                result = self.shutdownServer()
            elif command.startswith("/help"):
                result = self.commandsList()
            else:
                result = "Unknown server command. Valid commands are: " + self.commandsList()

        else:
            result = "Not Implemented"

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return dict(reply=result)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def play(self, id, demo=None):
        if demo is None or demo == "0":
            demos = vghd.ModelDemos[id]
            if len(demos) == 0:
                result = "no demo"
            else:
                plist = []
                for demo in demos:
                    plist.append((id, demo))
                self.listPlayer = vghd.listPlayer(plist)
                self.listPlayer.start()
                result = "Playing all"
        else:
            vghd.playDemo(id, demo)
            result = "ok"
        return dict(reply=result)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def nowplaying(self):
        return dict(reply=vghd.nowPlaying())

    def commandsList(self):
        """
        @return: list of available commands
        """
        html = Markup.page()

        html.h2("/help")
        html.p("Display this list of available commands.")

        html.h2("/shutdown")
        html.p("Shutdown the server.")

        return "{}".format(html)

    def shutdownServer(self):
        try:
            cherrypy.engine.exit()
        except:
            return "Shutdown Failed!"
        return "Shutting down..! This might take a minute."

