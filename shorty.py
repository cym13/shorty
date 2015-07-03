#!/usr/bin/python3

import time
import bottle
import pygments
import pygments.formatters
import pygments.lexers
import identigen
import config
from pathlib import Path


application      = bottle.default_app() # application used for wsgi mode
pygment_formater = pygments.formatters.HtmlFormatter(linenos="table")
dbpath           = Path(config.shortfile)


# Make sure our database file exists
dbpath.touch(mode=0o700)


@bottle.route('/')
def route_root():
    return bottle.template('root')


@bottle.route('/', method='POST')
def route_shorty_post():
    content = bottle.request.forms.getunicode('content', '') or ''
    sid     = identigen.generate(content)
    path    = dbpath / sid

    with path.open(mode='wb') as fd:
        fd.write(content.encode('utf8'))

    bottle.redirect('/' + sid)


@bottle.route('/static/<path:path>')
def route_static(path):
    return bottle.static_file(path, root='static')


@bottle.route('/favicon.ico')
def route_favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/robots.txt')
def route_robots():
    return bottle.static_file('robots.txt', root='static')


@bottle.route('/<sid>')
@bottle.route('/<sid>/<sformat>')
def route_shorty_get(sid, pformat='colored'):
    if pformat != 'colored' and pformat != 'raw':
        return bottle.template('bad_format')

    path = dbpath / sid

    try:
        with path.open(mode='rb') as fd:
            content = fd.read().decode('utf8')
    except IOError:
        # use this template for all file based exception
        bottle.abort(404)

    if pformat == 'colored':
        return bottle.template('shorty', content=content, sid=sid)

    # HTTP header
    bottle.response.content_type = 'text/plain; charset=UTF8'
    return content


@bottle.error(404)
def error404(error):
    return bottle.template("not_found")


@bottle.error(400)
def error400(error):
    return bottle.template("bad_request")


if __name__ == '__main__':
    print('I: Starting application with development server')
    bottle.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
else:
    print('I: Starting application as a wsgi application')
