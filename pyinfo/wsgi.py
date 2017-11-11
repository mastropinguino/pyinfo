# -*- coding: utf-8 -*-


def application(environ, start_response):
    import pyinfo

    output = pyinfo.info_as_html()

    start_response('200 OK', [('Content-type', 'text/html')])
    return [output.encode('utf-8')]
