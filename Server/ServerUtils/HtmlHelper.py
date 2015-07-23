from . import Markup


class HTMLHelper:
    def __init__(self, absdir, ipPort, pls=None):
        self.absDir = absdir
        self.ip_port = ipPort
        self.sl = Markup.oneliner  # returns a single html element
        if pls is None: pls = []
        self.playlists = pls

    def init(self, pageTitle="Home"):
        pageTitle = "PyVGDemo " + pageTitle

        navbar = """
            <table>
                <tr>
                    <td id="menu">
                        <ul>
                            <li class='side'><a href='/' class='menu'>Home</a></li>
                            <li class='side'><a href='javascript:search("name");' class='menu'>Search Name</a></li>
                            <li class='side'><a href='javascript:search("outfit");' class='menu'>Search Outfit</a></li>
                            <li class='side'><a href='javascript:search("id");' class='menu'>Search ID</a></li>
                            <li class='side'><a href='/help' class='menu'>Help &amp; Information</a></li>
                            <li class='side'><a href='/reload' class='menu'>Reload Models</a></li>
                            <li class='side'><a href='javascript:shutdown();' class='menu'>Shutdown</a></li>
                        </ul>
                        <hr/>
                        <div><small>
                        <a id='nowPlaying' href='#'></a>&nbsp;<a id='nowPlayingFunc' href='javascript:pl.NowPlaying();'></a>
                        </small></div>
                    </td>
                    <td>
                        <div id='main'>
                            <h1>PyVGDemo</h1>
        """
        
        footer = """
                        </div>
                    </td>
                    <td>
                        <div id='plContainer'>
                        <p><b>Playlists:</b></p>
                """

        # the playlists
        for i, pl in enumerate(self.playlists):
            name = pl.name
            
            if len(name) > 40:
                # if name is too large, take only the first 4 words
                # @todo: what if the name is not space separated?
                name = "&nbsp;".join(name.split()[:4]) + "..."

            footer +=   """<p class="plList" id="plList-{0}">"""\
                        """[<a class="plFunc" id="plFunc-{0}" href="javascript:pl.Func({0}, '{1}');">&gt;</a>]"""\
                        """&nbsp;<a class="plLink" id="plLink-{0}" href="/playlist?idx={0}">{1}</a>"""\
                        """</p>""".format(i, name.replace(" ", "&nbsp;"))

        footer += """<br/><a href="javascript:pl.Create();">Create&nbsp;Playlist</a>"""

        footer += """
                        </div>
                    </td>
                </tr>
            </table>
            <a href="#" class="scrollup">Scroll</a>
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
        html.p("""Nothing here! Please see the README.md for details.""")
        return "{}".format(html)
