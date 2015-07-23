import os
import cherrypy
from Server import Playlist
from Server.ServerUtils.HtmlHelper import HTMLHelper
from Server import vghd


class PlaylistHandler(object):
    def __init__(self, absDir, ip_port):
        self.pl = Playlist.PlaylistContainer(os.path.join(absDir, "Playlists"))
        self.pl.load()
        self.html = HTMLHelper(absDir, ip_port, self.pl.lists)

    @cherrypy.expose
    def show(self):
        # basically returns an empty page.
        self.html.playlists = self.pl.lists
        html = self.html.init("Playlists")
        return "{}".format(html)

    @cherrypy.expose
    def index(self, idx=None):
        # returns details of a playlist
        if idx is None:
            return self.show()
        idx = int(idx)
        html = self.html.init("Playlist {}".format(idx))
        html.p()
        html.b(self.pl.name(idx))
        html.add(" ({} clips)".format(self.pl.count(idx)))
        html.p.close()
        html.p()
        html.a("Play List", href="javascript:pl.Play({}, '{}');".format(idx, self.pl.name(idx)))
        html.a("Rename List", href="javascript:pl.Rename({}, '{}');".format(idx, self.pl.name(idx)))
        html.a("Delete List", href="javascript:pl.DeleteList({});".format(idx))
        html.a("Save Description", href="javascript:pl.Description({}, '{}');".format(idx, self.pl.name(idx)))
        html.p.close()
        html.hr()

        html.p()
        html.add("Description: ")
        html.br()
        html.textarea(id="plDesc")
        html.add(self.pl.getDesc(idx))
        html.textarea.close()
        html.p.close()

        html.p("List items: ")

        html.div(id="plListContainer")
        # send the current playlist id
        html.input(type="hidden", id="plistid", value=str(idx))
        html.ul()

        for no, clip in enumerate(self.pl.clips(idx)):
            clid, clname = clip
            # each li element id is: "card-id:clip-name"
            # we can use it later
            html.li(id="{}:{}".format(clid, clname))

            html.a(href="/card/{}".format(clid))
            html.img(src=r"/image/{0}/{0}c.jpg".format(clid), width="60px")
            html.a.close()
            html.a(href="javascript:play('{}', '{}');".format(clid, clname))
            html.h3(clname)
            html.a.close()

            # find the model name using the card
            model = vghd.search(id=clid)[0]
            html.p()
            html.b(model[1].title())
            html.p.close()

            html.small()
            html.a("Remove", href="javascript:pl.RemoveClip({}, '{}', '{}');".format(idx, clid, clname))
            html.a("Up", class_="reorder-up")
            html.a("Down", class_="reorder-down")
            html.small.close()

            html.li.close()

        html.ul.close()
        html.div.close()

        return "{}".format(html)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def play(self, idx):
        # play a specified playlist
        idx = int(idx)
        vghd.playList(self.pl.clips(idx))
        result = "Playing {} clips from {}.".format(self.pl.count(idx), self.pl.name(idx))
        return dict(reply=result)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def addclip(self, pl, id, name):
        # add a clip to the playlist
        pl = int(pl)
        if pl > self.pl.count():
            return dict(reply="Invalid playlist index.", status=0)
        self.pl.addClip(pl, id, name)
        self.pl.save(pl)
        return dict(reply="Clip added to {}".format(self.pl.name(pl)),
                    status=1)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create(self, name):
        self.pl.create(name)
        self.html.playlists = self.pl.lists
        return dict(reply="Playlist created.", plid=self.pl.count() - 1,
                    status=1)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def desc(self, idx, d):
        # save the description of a playlist
        idx = int(idx)
        self.pl.setDesc(idx, d)
        return dict(reply="Description set.", status=1)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def rename(self, idx, name):
        idx = int(idx)
        self.pl.rename(idx, name)
        self.html.playlists = self.pl.lists
        return dict(reply="Playlist renamed.", plid=self.pl.count() - 1,
                    status=1)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def removeclip(self, pl, id, name):
        pl = int(pl)
        if pl > self.pl.count():
            return dict(reply="Invalid playlist index.", status=0)

        self.pl.removeClip(pl, id, name)
        self.pl.save(pl)
        return dict(reply="Clip removed from {}".format(self.pl.name(pl)),
                    status=1)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def deletelist(self, pl):
        pl = int(pl)
        if pl > self.pl.count():
            return dict(reply="Invalid playlist index.", status=0)

        self.pl.remove(pl)
        self.html.playlists = self.pl.lists
        return dict(reply="Playlist deleted.", status=1)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def updateorder(self, idx, ids):
        # update the order of the clips of a playlist
        idx = int(idx)

        # the client side JS will send the ids of the
        # newly ordered clips seperated by "&"
        ids = ids.split("&")

        clips = []

        for line in ids:
            # each id has the format we set before in the li
            # element: "card-id:clip-name"
            if ":" in line:
                line = line.split(":")
                card = line[0].strip()
                cl = line[1].strip()
                clips.append((card, cl))

        if self.pl.updateOrder(idx, clips):
            self.html.playlists = self.pl.lists
            return dict(reply="Order updated.", status=1)
        else:
            # this might happen if the list of ids are invalid
            return dict(reply="Order NOT updated.", status=0)
