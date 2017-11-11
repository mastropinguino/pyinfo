# -*- coding: utf-8 -*-
import cgi


PAGE_HTML = """
<!DOCTYPE html>
<html>
    <head>
    <title>pyinfo()</title>
    <meta name="robots" content="noindex,nofollow,noarchive,nosnippet">
    {style}
    </head>
    <body>
        <div class="center">
        {h.section_title}

        <h2>System</h2>
        {h.section_system}

        <h2>Python Internals</h2>
        {h.section_py_internals}

        <h2>OS Internals</h2>
        {h.section_os_internals}

        <h2>WSGI Environment</h2>
        {h.section_environ}

        <h2>Database support</h2>
        {h.section_database}

        <h2>Compression and archiving</h2>
        {h.section_compression}

        {h.section_ldap}

        {h.section_socket}

        <h2>Multimedia support</h2>
        {h.section_multimedia}

        <h2>Copyright</h2>
        {h.section_copyright}

        </div>
    </body>
</html>
"""

PAGE_STYLE = """
    <style type="text/css">
     body{background-color:#fff;color:#000}
     body,td,th,h1,h2{font-family:sans-serif}
     pre{margin:0px;font-family:monospace}
     a:link{color:#009;text-decoration:none;background-color:#fff}
     a:hover{text-decoration:underline}
     table{border-collapse:collapse}
     .center{text-align:center}
     .center table{margin-left:auto;margin-right:auto;text-align:left}
     .center th{text-align:center !important}
     td,th{border:1px solid #999999;font-size:75%;vertical-align:baseline}
     h1{font-size:150%}
     h2{font-size:125%}
     .p{text-align:left}
     .e{width:30%;background-color:#ffffcc;font-weight:bold;color:#000}
     .h{background:url('http://python.org/images/header-bg2.png') repeat-x;font-weight:bold;color:#000}
     .v{background-color:#f2f2f2;color:#000}
     .vr{background-color:#cccccc;text-align:right;color:#000}
     img{float:right;border:0px;}
     hr{width:600px;background-color:#ccc;border:0px;height:1px;color:#000}
    </style>
"""


class HtmlHelpers():
    def __init__(self, info):
        self.info = info

    def table(self, html):
        return '<table border="0" cellpadding="3" width="600">%s</table><br>' % html

    def maketable(self, data):
        html = ''
        for k in data:
            v = cgi.escape(str(data[k]))
            html += '<tr><td class="e">%s</td><td class="v">%s</td></tr>' % (k, v)
        return self.table(html)

    @property
    def section_title(self):
        html = '<tr class="h"><td>'
        html += '<a href="http://python.org/"><img border="0" src="http://python.org/images/python-logo.gif"></a>'
        html += '<h1 class="p">Python %s</h1>' % self.info['System information']['Python version']
        html += '</td></tr>'
        return self.table(html)

    @property
    def section_system(self):
        return self.maketable(self.info['System information'])

    @property
    def section_py_internals(self):
        return self.maketable(self.info['Python internals'])

    @property
    def section_os_internals(self):
        return self.maketable(self.info['OS internals'])

    @property
    def section_environ(self):
        return self.maketable(self.info['Environment variables'])

    @property
    def section_database(self):
        return self.maketable(self.info['Database support'])

    @property
    def section_compression(self):
        return self.maketable(self.info['Compression and archiving'])

    @property
    def section_ldap(self):
        if 'LDAP support' not in self.info:
            return ''

        html = self.maketable(self.info['LDAP support'])
        return '<h2>LDAP support</h2>' + html

    @property
    def section_socket(self):
        if 'Socket' not in self.info:
            return ''
        html = self.maketable(self.info['Socket'])
        return '<h2>Socket</h2>' + html

    @property
    def section_multimedia(self):
        return self.maketable(self.info['Multimedia support'])

    @property
    def section_copyright(self):
        text = self.info['Copyright'].replace('\n\n', '<br>') \
            .replace('\r\n', '<br />').replace('(c)', '&copy;')
        return self.table('<tr class="v"><td>%s</td></tr>' % text)


def render_html(info):
    """Return the HTML page version of pyinfo."""
    helper = HtmlHelpers(info)
    return PAGE_HTML.format(h=helper, style=PAGE_STYLE)


def _guess_max_lengths(info):
    """Compute the maximum length for keys and lines."""
    max_key_len = 0
    max_line_len = 0

    for sec in info:
        for k in info[sec]:
            l_k = len(k)
            l_data = len(info[sec])
            line_len = l_k + 2 + l_data
            if line_len > 80:
                # skip lines which wraps
                continue

            if line_len > max_line_len:
                # found a bigger line length
                max_line_len = line_len

            if l_k > max_key_len:
                # Found a bigger key length
                max_key_len = l_k

    return (max_key_len, max_line_len)


def render_text(info):
    """Create the text version of pyinfo."""
    d = []
    max_key_len, max_line_len = _guess_max_lengths(info)

    for sec in info:
        # build section title (2 = spaces for padding)
        title_size = len(sec)
        sym = "=" * int((max_line_len - title_size - 2) / 2)
        d += ["{} {} {}".format(sym, sec, sym)]

        sec_info = info[sec]

        if sec == 'Copyright':
            # customize the output for global section because of long copyright
            d += [sec_info]
            continue
        fmt = "{:>%s}: {}" % (max_key_len,)
        for k in sec_info:
            d += [fmt.format(k, sec_info[k])]
        d += [""]

    return "\n".join(d)
