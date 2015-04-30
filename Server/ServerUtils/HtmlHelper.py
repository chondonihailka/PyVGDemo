from . import Markup

class HTMLHelper():
    def __init__(self, absdir, ipPort):
        self.absDir = absdir
        self.ip_port = ipPort
        self.sl = Markup.oneliner #returns a single html element

    def init(self, pageTitle="Home"):
        pageTitle = "PyVGHD " + pageTitle
        navbar = """
            <table>
                <tr>
                    <td id="menu">
                        <ul>
                            <li class='side'><a href='/' class='menu'>Home</a></li>
                            <li class='side'><a href='/cards' class='menu'>All Models</a></li>
                            <li class='side'><a href='javascript:findModel();' class='menu'>Find Model</a></li>
                            <li class='side'><a href='/settings' class='menu'>Settings</a></li>
                            <li class='side'><a href='/help' class='menu'>Help &amp; Information</a></li>
                            <li class='side'><a href='/ajax/?command=/shutdown' class='menu'>Shutdown</a></li>
                        </ul>
                    </td>
                    <td>
                        <div id='main'>
                            <h1>PyVGHD</h1>
        """
        footer = """
                        </div>
                    </td>
                </tr>
            </table>
        """
        html = Markup.page()
        html.init(title=pageTitle,
           header=navbar,
           footer=footer,
           script=["/media/jquery/", "/media/cherryjs/", "/media/js/"],
           css=["/media/css/", "/media/vghdcss/"]
        )
        return html

    def helpInstruction(self):
        html = self.init("Help and Instructions")
        html.h2("Help and Information")
        html.p("""Not Implemented""")
        return "{}".format(html)
