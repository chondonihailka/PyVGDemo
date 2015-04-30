import subprocess
import threading
from os import environ as env
from os.path import join as pj
from os.path import isfile


def ShellExecute(cmd):
    """
    Executes a command in the system shell. The terminal will not pop up.
    Execution is done on a seperate thread for non-blocking.
    @param cmd: command to execute
    @return: response of the system
    """
    class _shell_thread(threading.Thread):
        def __init__(self, cmdp):
            threading.Thread.__init__(self)
            self.daemon = True
            self.setName("Shell Execute")
            self.cmd = cmdp
            self.respose = ""

        def run(self):
            try:
                self.respose = subprocess.check_output(self.cmd, shell=True)
            except:
                self.respose = "Execution failed!"

    shell = _shell_thread(cmd)
    shell.start()


def launchAsChromeApp(url):
    chrome = None
    path86 = pj(env["SYSTEMDRIVE"], "\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
    path64 = pj(env["SYSTEMDRIVE"], "\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    if isfile(path86):
        chrome = path86
    elif isfile(path64):
        chrome = path64

    if chrome:
        ShellExecute('"{}" -app={}'.format(chrome, url))
    else:
        ShellExecute("start {}".format(url))
