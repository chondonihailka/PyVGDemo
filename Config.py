import os

try:
    from _winreg import HKEY_USERS
except ImportError:
    from winreg import HKEY_USERS

ip_port = ("localhost", 56021)
start_browser = True

vdhd_data = "R:\\VGHD\\data"
vghd_models = "E:\\VG Backup\\models"
vdhd_exe = os.path.join(os.environ["LOCALAPPDATA"], "vghd\\bin\\vghd.exe")

regHead = HKEY_USERS
regId = r"S-1-5-21-9263988-149312531-499419475-1001"
regLoc = regId + r"\Software\Totem\vghd\Parameters"
regClipLoc = regId + r"\Software\Totem\vghd\player"

models_sorted = False