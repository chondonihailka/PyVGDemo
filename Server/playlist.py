import os
import random

class Playlist:
    def __init__(self, path):
        self.path = path
        self.clips = []
        n = os.path.basename(self.path).split(".")[:-1]
        self.name = ".".join(n)
        self.desc = ""

    def load(self):
        with open(self.path) as pl:
            for line in pl:
                line = line.strip()
                if line.startswith("#"):
                    self.desc += line.strip('#')
                    continue
                if line == "":
                    continue
                if "," in line:
                    line = line.split(",")
                    idx = line[0].strip()
                    cl = line[1].strip()
                    self.clips.append((idx, cl))

    def delete(self):
        os.remove(self.path)

    def rename(self, name):
        new = os.path.join(os.path.dirname(self.path), name)
        os.rename(self.path, new)
        self.path = new
        n = name.split(".")[:-1]
        self.name = ".".join(n)

    def save(self):
        with open(self.path, 'w+') as pl:
            desc = self.desc.replace("\n", "\n#")
            pl.write("#{}\n\n".format(desc))
            for item in self.clips:
                idx, cl = item
                pl.write("{}, {}\n".format(idx, cl))

    def addClip(self, idx, clip):
        self.clips.append((idx, clip))

    def removeClipAt(self, idx):
        del self.clips[idx-1]

    def removeClip(self, cardid, clipname):
        try:
            idx = self.clips.index((cardid, clipname))
        except ValueError: return
        else: del self.clips[idx]

    def shuffle(self):
        random.shuffle(self.clips)


class PlaylistContainer:
    def __init__(self, directory=None):
        self.listdir = directory
        self.playlist_extension = ".pl"
        self.lists = []

    def load(self, directory=None):
        if directory:
            self.listdir = directory
        if self.listdir is None:
            raise ValueError("List directory is not set.")
        if not os.path.isdir(self.listdir):
            os.mkdir(self.listdir)
        for f in os.listdir(self.listdir):
            if f.endswith(self.playlist_extension):
                hnd = Playlist(os.path.join(self.listdir, f))
                hnd.load()
                self.lists.append(hnd)

    def getIdByName(self, name):
        for i, l in enumerate(self.lists):
            if name == l.name:
                return i
        return None

    def getIdByPath(self, path):
        for i, l in enumerate(self.lists):
            if path == l.path:
                return i
        return None

    def create(self, name):
        if not name.endswith(self.playlist_extension):
            name += self.playlist_extension
        hnd = Playlist(os.path.join(self.listdir, name))
        hnd.save()
        self.lists.append(hnd)
        return hnd

    def rename(self, playlistid, name):
        if not name.endswith(self.playlist_extension):
            name += self.playlist_extension
        self.lists[playlistid].rename(name)

    def addClip(self, playlistid, cardid, clipname):
        self.lists[playlistid].addClip(cardid, clipname)

    def name(self, playlistid):
        return self.lists[playlistid].name

    def getDesc(self, playlistid):
        return self.lists[playlistid].desc

    def setDesc(self, playlistid, d):
        self.lists[playlistid].desc = d
        self.lists[playlistid].save()

    def clips(self, playlistid):
        return self.lists[playlistid].clips

    def save(self, playlistid=None):
        if playlistid is None:
            for l in self.lists:
                l.save()
        else:
            self.lists[playlistid].save()

    def removeClip(self, playlistid, cardid, name):
        self.lists[playlistid].removeClip(cardid, name)
        self.save(playlistid)

    def remove(self, playlistid):
        self.lists[playlistid].delete()
        del self.lists[playlistid]

    def count(self, playlistid=None):
        if playlistid is None:
            return len(self.lists)
        else:
            return len(self.lists[playlistid].clips)

    def updateOrder(self, playlistid, newlist):
        if len(newlist) != self.count(playlistid):
            # print("UO: length mismatch.")
            return False
        for newitem in newlist:
            if newitem not in self.lists[playlistid].clips:
                # print("UO: {} not in {}".format(newitem, self.name(playlistid)))
                return False
        self.lists[playlistid].clips = newlist
        self.save(playlistid)
        return True
