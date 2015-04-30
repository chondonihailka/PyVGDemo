import os

try:
    import _winreg as winreg
except ImportError:
    import winreg

import cherrypy
import Config as cfg
from . import vghd
from .ServerUtils.HtmlHelper import HTMLHelper
from .ServerUtils import ConfigPHelper


class SettingsHandler(object):
    def __init__(self, direc):
        self.absDir = direc
        self.html = HTMLHelper(direc, cfg.ip_port)

    @cherrypy.expose
    def index(self):
        html = self.html.init("Settings")
        html.h2("Please review the following settings.")
        html.form(method="post", id="settingsForm", action="#")
        html.p("VGHD data directory: ")
        html.input(type="text", size="100", id="vgdata", name="vgdata", value=cfg.vdhd_data)
        html.br()
        html.p("VGHD models directory: ")
        html.input(type="text", size="100", id="vgmodels", name="vgmodels", value=cfg.vghd_models)
        html.br()
        html.p("VGHD executable path: ")
        html.input(type="text", size="100", id="vgexe", name="vgexe", value=cfg.vdhd_exe)
        html.br()
        html.p("Windows user ID: ")
        html.input(type="text", size="100", id="winid", name="winid", value=cfg.regId)
        html.br()
        html.input(type="submit", value="Save Settings", class_="pb blue")
        html.form.close()
        html.script(src="/media/settings.js", type="text/javascript")
        html.script.close()
        return "{}".format(html)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def checkpath(self, path):
        if os.path.exists(path):
            reply = "true"
        else:
            reply = "false"
        return dict(reply=reply)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def checkregkey(self, key):
        try:
            winreg.OpenKey(winreg.HKEY_USERS, key, 0, winreg.KEY_ALL_ACCESS)
            reply = "true"
        except WindowsError:
            reply = "false"
        return dict(reply=reply)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def save(self, vgdata, vgmodels, vgexe, winid):
        config = ConfigPHelper.Configuration(self.absDir)
        config.setValue("vghd_data_dir", vgdata, "virtuagirl")
        config.setValue("vghd_models_dir", vgmodels, "virtuagirl")
        config.setValue("vghd_executable", vgexe, "virtuagirl")
        config.setValue("windows_user_id", winid, "virtuagirl")
        config.Save()
        vghd.Load()
        idxbld = vghd.index_builder()
        idxbld.start()
        return dict(reply="Settings saved successfully.")

    def load(self):
        config = ConfigPHelper.Configuration(self.absDir)
        if config.exists():
            cfg.vdhd_data = config.getValue("vghd_data_dir", "virtuagirl")
            cfg.vghd_models = config.getValue("vghd_models_dir", "virtuagirl")
            cfg.vdhd_exe = config.getValue("vghd_executable", "virtuagirl")
            cfg.regId = config.getValue("windows_user_id", "virtuagirl")
        vghd.Load()
        idxbld = vghd.index_builder()
        idxbld.start()
