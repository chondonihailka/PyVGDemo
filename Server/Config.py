import os

try:
    import _winreg as winreg
except ImportError:
    import winreg

# the ip and port to serve
ip_port = ("127.0.0.1", 8088)

# should the browser be started automatically
start_browser = True

# the path to Virtuagirl models data directory.
# Contains all the models directories with their pictures inside.
# This directory can be changed from the defualt during installation.
vdhd_data = None

# the path to the directory of the clips.
# This directory can be changed from Virtuagirl settings.
vghd_models = None

# the path to the Virtuagirl executable
vdhd_exe = None

# the registry head where Virtuagirl settings are stored.
# this is by default HKEY_USERS
regHead = winreg.HKEY_USERS

# HKEY_USERS may contain more than one sub key
# only one of them got the Virtuagirl settings
regId = None

# relative location of the Virtuagirl settings in the registry
regLoc = r"\Software\Totem\vghd\Parameters"
regClipLoc = r"\Software\Totem\vghd\player"
regSystemLoc = r"\Software\Totem\vghd\System"

models_sorted = False
