import os
import re
import threading
import time
from os.path import join as pj

try:
    import _winreg as winreg
except ImportError:
    import winreg

import Server.Config as cfg
from Server.ServerUtils import ThreadUtils

ModelDirs = {}
ModelDemos = {}
SearchIndex = ""
__list_player = None


class model(object):
    # Needed regex for parsing model info
    name = re.compile(r"<name>(.*?)</name>")
    id = re.compile(r"<id>(.*?)</id>")
    desc = re.compile(r"<description>(.*?)</description>")
    country = re.compile(r"<country>(.*?)</country>")
    city = re.compile(r"<city>(.*?)</city>")
    outfit = re.compile(r"<outfit>(.*?)</outfit>")


def Load():
    # parse the xmls and (re)build the models and clips index
    global ModelDemos, ModelDirs
    ModelDirs = {}
    ModelDemos = {}

    if cfg.vdhd_data is None:
        return

    for dir_name in os.listdir(cfg.vdhd_data):
        # inside the vghd data dir,
        # each dir is named as the card no,
        model_dir = pj(cfg.vdhd_data, dir_name)
        if os.path.isdir(model_dir):
            # for each such dir,
            for file_item in os.listdir(model_dir):
                # if there is an xml file,
                if file_item.endswith(".xml") and "cache" not in file_item:
                    # store the dir.
                    ModelDirs[dir_name] = model_dir
                    ModelDemos[dir_name] = []
                    demo_dir = pj(cfg.vghd_models, dir_name)
                    # if a same dir exists inside the vghd models dir,
                    if os.path.isdir(demo_dir):
                        # store the clips.
                        for demo_file in os.listdir(demo_dir):
                            # we will need to change here if we want 
                            # to include more than demo files
                            if demo_file.endswith(".demo"):
                                ModelDemos[dir_name].append(demo_file)


def getModels(st, end):
    # return a list of clips within the range given
    if end > len(ModelDemos):
        end == len(ModelDemos)
    if cfg.models_sorted:
        keys = sorted(ModelDemos)[st:end]
    else:
        keys = list(ModelDemos.keys())[st:end]
    temp = {}
    for k in keys:
        temp[k] = ModelDirs[k]
    return temp


def getCardImg(card):
    # return the path to the model image for given id
    modeldir = ModelDirs[card]
    x = pj(modeldir, "{}_full.png".format(card))
    y = pj(modeldir, "{}_full.jpg".format(card))
    if os.path.isfile(x):
        return x
    elif os.path.isfile(y):
        return y
    else:
        return "Not Found!"


class ModelInfo:
    # class for parsing all the model info

    def __init__(self, card):
        self.id = card
        self.xml = ""
        if card in ModelDirs:
            directory = ModelDirs[card]
            xfile = pj(directory, "{}.xml".format(card))
            if os.path.isfile(xfile):
                xfile = open(xfile)
                self.xml = xfile.read()
                xfile.close()

    def name(self):
        res = re.findall(model.name, self.xml)
        if len(res) == 0:
            return "No name"
        else:
            return res[0]

    def cards(self):
        return re.findall(model.id, self.xml)

    def collectedCards(self):
        ids = []
        for card in self.cards():
            if card in ModelDemos and card != self.id:
                if card not in ids:
                    ids.append(card)
        return ids

    def country(self):
        res = re.findall(model.country, self.xml)
        if len(res) == 0:
            return "No country"
        else:
            return res[0]

    def city(self):
        res = re.findall(model.city, self.xml)
        if len(res) == 0:
            return "No city"
        else:
            return res[0]

    def outfit(self):
        res = re.findall(model.outfit, self.xml)
        if len(res) == 0:
            return "No outfit"
        else:
            return res[0]

    def description(self):
        res = re.findall(model.desc, self.xml)
        if len(res) == 0:
            return "No description"
        else:
            return res[0]


class index_builder(threading.Thread):
    # a threaded search index builder
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.setName("Index Builder")

    def run(self):
        global SearchIndex
        for id_no in ModelDirs:
            mdl = ModelInfo(id_no)
            # SearchIndex is just a line feed seperated string containing all the
            # models info as in the following format. We can then use regex to
            # search this string.
            SearchIndex += "id:{};name:{};outfit:{};city:{};country:{};\n".format(
                id_no, mdl.name(), mdl.outfit(), mdl.city(), mdl.country()
            ).lower()


def search(**kwargs):
    # search the models info using regex in the SearchIndex
    # return a list of all found mathces.
    idx = name = outfit = city = coun = ""
    if "id" in kwargs:
        idx = kwargs["id"].lower()
    if "name" in kwargs:
        name = kwargs["name"].lower()
    if "city" in kwargs:
        city = kwargs["city"].lower()
    if "outfit" in kwargs:
        outfit = kwargs["outfit"].lower()
    if "country" in kwargs:
        coun = kwargs["country"].lower()
    return re.findall(
        re.compile(r"id:(.*?{}.*?);name:(.*?{}.*?);outfit:(.*?{}.*?);city:(.*?{}.*?);country:(.*?{}.*?);".format(
            idx, name, outfit, city, coun)
        ),
        SearchIndex
    )


def playDemo(card, demo):
    # play a specific demo under a model id
    if demo not in ModelDemos[card]:
        return False
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regLoc, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "ForceAnim", 0, winreg.REG_SZ, "{}\\{}".format(card, demo))
    return True


def nowPlaying():
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "CurrentAnim")[0]

def dataDir():
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regSystemLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "DataPath")[0]

def modelsDir():
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regSystemLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "ModelsPath")[0]

def exePath():
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regSystemLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "MainPath")[0] + "\\vghd.exe"

def isPlaying():
    # is vghd currently playing clip?
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regLoc, 0, winreg.KEY_ALL_ACCESS)
    res = winreg.QueryValueEx(key, "WindowPlayer")
    return res[0] == 1


def currentClips():
    # return a list of clips currently being played
    key = winreg.OpenKey(cfg.regHead, cfg.regId + cfg.regClipLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "currentClips")[0]


class _listPlayer(ThreadUtils.ControlledThread):
    # a thread to play clips sequentially
    def __init__(self, plist):
        ThreadUtils.ControlledThread.__init__(self)
        self.plist = plist
        self.currentAnim = None
        self.playstarted = False
        self.i = 0
        #print("List:: will play {}".format(self.plist))

    def do_work(self):
        if self.playstarted and not isPlaying():
            # The list has started playing, but its not
            # playing now. That means vghd has been turned off
            print("List:: stopped.")
            self.finish()
        else:
            if self.i < len(self.plist):
                # print("CurrAnim: {} Clips: {}".format(self.currentAnim, currentClips().split()))
                if self.currentAnim in currentClips().split():
                    # wait. our clip is still playing
                    time.sleep(1)
                else:
                    # take the next clip from the list
                    item = self.plist[self.i]
                    card = item[0]
                    clip = item[1]
                    self.currentAnim = "{}".format(clip)
                    print("List:: Playing {}".format(clip))
                    # play it
                    playDemo(card, clip)

                    # check if the clip has started playing every half sec,
                    # max wait 10 * 0.5 = 5 secs
                    wait = 10
                    while self.currentAnim not in currentClips().split() and wait:
                        time.sleep(0.5)
                        wait -= 1

                    self.playstarted = True
                    self.i += 1
                    time.sleep(1)
            else:
                print("List:: finished.")
                self.finish()


def playList(plist):
    # Play the list of clips given.
    # A seperate thread is spawned to control it.
    # If a list is being played, it is stopped.

    global __list_player

    if __list_player and __list_player.isAlive():
        __list_player.stop()

    __list_player = _listPlayer(plist)
    __list_player.start()

    return __list_player


def getDemoIds(demos):
    # a helper function to extract the card nos from the
    # given list of demos. Return the list of card nos.
    ids = []
    for demo in demos:
        ids.append(demo.split(".")[0].split("_")[1])
    return ids
