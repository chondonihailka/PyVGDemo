import os
import re
import time
from os.path import join as pj
try:
    import _winreg as winreg
except NameError:
    import winreg

import Config as cfg
from . import ThreadUtils

ModelDirs = {}
ModelDemos = {}

class model(object):
    name = re.compile(r"<name>(.*?)</name>")
    id = re.compile(r"<id>(.*?)</id>")
    desc = re.compile(r"<description>(.*?)</description>")
    country = re.compile(r"<country>(.*?)</country>")
    city = re.compile(r"<city>(.*?)</city>")

def Load():
    global ModelDemos, ModelDirs
    ModelDirs = {}
    ModelDemos = {}

    if cfg.vdhd_data is None:
        return

    for dir_name in os.listdir(cfg.vdhd_data):
        model_dir = pj(cfg.vdhd_data, dir_name)
        if os.path.isdir(model_dir):
            for file_item in os.listdir(model_dir):
                if file_item.endswith(".xml"):
                    ModelDirs[dir_name] = model_dir
                    ModelDemos[dir_name] = []
                    demo_dir = pj(cfg.vghd_models, dir_name)
                    if os.path.isdir(demo_dir):
                        for demo_file in os.listdir(demo_dir):
                            if demo_file.endswith(".demo"):
                                ModelDemos[dir_name].append(demo_file)
                    if len(ModelDemos[dir_name]) == 0:
                        del(ModelDemos[dir_name])

def getModels(st, end):
    if end > len(ModelDemos):
        end == len(ModelDemos)
    keys = sorted(ModelDemos)[st:end]
    temp = {}
    for k in keys:
        temp[k] = ModelDirs[k]
    return temp

def getCardImg(id):
    dir = ModelDirs[id]
    x = pj(dir, "{}_full.png".format(id))
    y = pj(dir, "{}_full.jpg".format(id))
    if os.path.isfile(x): return x
    elif os.path.isfile(y): return y
    else: return "Not Found!"

class ModelInfo():
    def __init__(self, id):
        self.id = id
        self.xml = ""
        if id in ModelDirs:
            directory = ModelDirs[id]
            xfile = pj(directory, "{}.xml".format(id))
            xfile = open(xfile)
            self.xml = xfile.read()
            xfile.close()

    def name(self):
        res = re.findall(model.name, self.xml)
        if len(res) == 0:
            return "No name found!"
        else:
            return res[0]

    def ids(self):
        return re.findall(model.id, self.xml)

    def collectedIds(self):
        ids = []
        for id in self.ids():
            if id in ModelDemos and id != self.id:
                if id not in ids:
                    ids.append(id)
        return ids

    def country(self):
        res = re.findall(model.country, self.xml)
        if len(res) == 0:
            return "No country found!"
        else:
            return res[0]

    def city(self):
        res = re.findall(model.city, self.xml)
        if len(res) == 0:
            return "No city found!"
        else:
            return res[0]

    def description(self):
        res = re.findall(model.desc, self.xml)
        if len(res) == 0:
            return "No description found!"
        else:
            return res[0]

def playDemo(id, demo):
    if demo not in ModelDemos[id]:
        return False
    key = winreg.OpenKey(cfg.regHead, cfg.regLoc, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "ForceAnim", 0, winreg.REG_SZ, "{}\\{}".format(id, demo))
    return True

def nowPlaying():
    key = winreg.OpenKey(cfg.regHead, cfg.regLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "CurrentAnim")

def currentClips():
    key = winreg.OpenKey(cfg.regHead, cfg.regClipLoc, 0, winreg.KEY_ALL_ACCESS)
    return winreg.QueryValueEx(key, "currentClips")

class listPlayer(ThreadUtils.ControlledThread):
    def __init__(self, plist):
        ThreadUtils.ControlledThread.__init__(self)
        self.plist = plist
        self.currentAnim = None

    def do_work(self):
        if len(self.plist) > 0:
            # print("CurrAnim: {} Clips: {}".format(self.currentAnim, currentClips()[0]))
            if self.currentAnim in currentClips()[0].split():
                time.sleep(1)
            else:
                item = self.plist.pop(0)
                id = item[0]
                demo = item[1]
                self.currentAnim = "{}".format(demo)
                playDemo(id, demo)
                time.sleep(2)
        else:
            self.finish()

def getDemoIds(demos):
    ids = []
    for demo in demos:
        ids.append(demo.split(".")[0].split("_")[1])
    return ids
