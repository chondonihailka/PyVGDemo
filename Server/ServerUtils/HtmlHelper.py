from . import Markup


class HTMLHelper():
    def __init__(self, absdir, ipPort):
        self.absDir = absdir
        self.ip_port = ipPort
        self.sl = Markup.oneliner  # returns a single html element

    def init(self, pageTitle="Home"):
        pageTitle = "PyVGHD " + pageTitle
        navbar = """
            <table>
                <tr>
                    <td id="menu">
                        <ul>
                            <li class='side'><a href='/' class='menu'>Home</a></li>
                            <li class='side'><a href='/cards' class='menu'>All Models</a></li>
                            <li class='side'><a href='javascript:search("name");' class='menu'>Search Name</a></li>
                            <li class='side'><a href='javascript:search("outfit");' class='menu'>Search Outfit</a></li>
                            <li class='side'><a href='javascript:search("id");' class='menu'>Search ID</a></li>
                            <li class='side'><a href='/settings' class='menu'>Settings</a></li>
                            <li class='side'><a href='/help' class='menu'>Help &amp; Information</a></li>
                            <li class='side'><a href='javascript:shutdown();' class='menu'>Shutdown</a></li>
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
                  script=["/media/jquery.js", "/media/sweet/sweetalert.min.js", "/media/default.js"],
                  css=["/media/default.css", "/media/sweet/sweetalert.css"]
        )
        return html

    def helpInstruction(self):
        html = self.init("Help and Instructions")
        html.h2("Help and Information")
        html.p("""Not Implemented""")
        return "{}".format(html)
