import os
import sys

#FREEZING REQUIREMENTS
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.join(os.path.dirname(sys.executable),'bin'))
    sys.path.append(os.path.join(os.path.dirname(sys.executable),'bin\\library.zip'))
    absDir = os.path.join(os.getcwd(), os.path.dirname(sys.executable))
else:
    absDir = os.path.join(os.getcwd())
#FREEZING REQUIREMENTS

from Server.CherryServer import StartServer

if __name__ == '__main__':
    StartServer(absDir)