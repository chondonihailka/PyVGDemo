import cherrypy

from Server.ServerUtils import Markup
from Server import vghd


class AjaxHandler(object):
    def __init__(self, absDir):
        self.absDir = absDir

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
        # Play a clip from an specific model

        if demo is None or demo == "0":
            # if no clip was specified, we will load all the clips
            # from the model and play them as a playlist
            demos = vghd.ModelDemos[id]
            if len(demos) == 0:
                result = "No demo found for {}.".format(id)
            else:
                plist = []
                for demo in demos:
                    plist.append((id, demo))

                vghd.playList(plist)
                result = "Playing {} demos from {}.".format(len(demos), id)
        else:
            vghd.playDemo(id, demo)
            result = "Playing demo {} from {}.".format(demo, id)
        return dict(reply=result)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def nowplaying(self):
        # return the info about the clip currently playing
        anim = vghd.nowPlaying()
        if "\\" in anim:
            mid = anim.split("\\")[0]
            clip = anim.split("\\")[1]
            return dict(clip=clip, id=mid)
        else:
            return dict(clip="", id="")

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
        return "Shutting down ... This might take a minute."

