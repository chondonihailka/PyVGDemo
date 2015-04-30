import os
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

class Configuration(object):
    def __init__(self, absdir, filename="settings.ini"):
        self.absDir = absdir
        self.configFile = os.path.join(self.absDir, filename)
        self.config = ConfigParser()
        self.__readConfiguration()

    def __readConfiguration(self):
        if os.path.isfile(self.configFile):
            self.config.read(self.configFile)

    def getValue(self, variable, section="main", default=None, datatype="string"):
        if not self.config.has_option(section, variable):
            return default
        if datatype=="int":
            return self.config.getint(section, variable)
        elif datatype=="float":
            return self.config.getfloat(section, variable)
        elif datatype=="bool":
            return self.config.getboolean(section, variable)
        else:
            return self.config.get(section, variable)

    def setValue(self, variable, value, section="main"):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, variable, value)

    def Delete(self, variable, section="main"):
        if self.config.has_option(section, variable):
            self.config.remove_option(section, variable)

    def Save(self):
        with open(self.configFile, 'w+') as configfile:    # save
            self.config.write(configfile)

    def exists(self):
        return os.path.isfile(self.configFile)