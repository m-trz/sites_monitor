"""
Author: Marcin Trzcinski

Script checking website status

It includes a simple web server with last checks results
available at 'localhost:PORT' address at port specified below.

All results are logged to 'checks.log' file.
Websites with tests to be checked can be configured in 'config.py' file.
"""

from argparse import ArgumentParser
import logging
import logging.handlers

from gevent import monkey
monkey.patch_all()

import gevent
from gevent.wsgi import WSGIServer
from gevent.lock import BoundedSemaphore
import requests

import config



PORT = 8000
INTERVAL = 5

states_lock = BoundedSemaphore(1)
STATES = {}


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.handlers.TimedRotatingFileHandler(filename='checks.log', when='D')
fh.setLevel(logging.INFO)
fmt = logging.Formatter(fmt='[%(levelname)s] %(asctime)s: %(message)s')
fh.setFormatter(fmt)
logger.addHandler(fh)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter(fmt='%(message)s'))
logger.addHandler(sh)


def status_worker(site, text, interval):
    while True:
        status, duration = check_status(site, text)
        msg = '{:40}{:^32}{:6.2f}'.format(site, status, duration)
        logger.info(msg)
        with states_lock:
            STATES[site] = (status, duration)
        gevent.sleep(interval - duration)


def check_status(address, text):
    """Sends request to address and checks if text is present in reponse

    Args:
        address (str): site address
        text (str): text to be checked in responce

    Returns:
        (status, elapsed): (tuple (str, int)) with status, and responce time
    """

    elapsed = 0
    try:
        r = requests.get(address)
    except requests.ConnectionError:
        status = "Error: CONNECTION_ERROR"
    except Exception as e:
        status = 'Error: {}'.format(str(e))
    else:
        if r.status_code == 200:
            status = 'OK' if text in r.text else 'Error: CON_OK_MISSING_TEXT'
        else:
            status = 'Error: {}'.format(r.status_code)
        elapsed = r.elapsed.total_seconds()

    return status, elapsed


def application(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html')
    ]

    body = [('<h1>Website Status Monitor</h1>' +
             '<table>' +
             '<tr><td>Name</td><td>Status</td><td>Response Time [s]</td></tr>'
             )]

    with states_lock:
        for k, v in STATES.items():
            body.append('<tr><td>{k}</td><td>{v[0]}</td><td>{v[1]}</td></tr>'
                        .format(k=k, v=v))
    body.append('</table>')

    start_response(status, headers)

    return [''.join(body).encode()]


def main():

    parser = ArgumentParser(description='Tool monitoring sites status')
    parser.add_argument('--interval', type=int, default=INTERVAL,
                        help=('Time interval in seconds between status ' +
                              'checks (default: {})'.format(INTERVAL)))
    parser.add_argument('--port', type=int, default=PORT,
                        help='Server port (default: {})'.format(PORT))

    args = parser.parse_args()
    interval = args.interval
    port = args.port

    logging.info('Script starting with time interval={}, port={}'
                 .format(interval, port))

    gevent.iwait(
        [gevent.spawn(status_worker, site, text, interval)
         for site, text in config.sites])

    WSGIServer(('', port), application).serve_forever()


if __name__ == '__main__':
    main()
