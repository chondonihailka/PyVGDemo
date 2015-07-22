import os
import sys

# FREEZING REQUIREMENTS
if getattr(sys, 'frozen', False):
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'bin'))
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'bin\\library.zip'))
    absDir = os.path.join(os.getcwd(), os.path.dirname(sys.executable))
else:
    absDir = os.getcwd()
#FREEZING REQUIREMENTS

from Server.CherryServer import StartServer

if __name__ == '__main__':
    try:
        import cherrypy
    except (ImportError, NameError):
        input("""Error: Can not find the module 'cherrypy'.

        PyVGDemo depends on CherryPy.
        Please install CherryPy first. You can install it using pip.
        Execute "pip install cherrypy" in your command prompt.
        Or visit http://www.cherrypy.org for other options.
        """)
    else:
        StartServer(absDir)
