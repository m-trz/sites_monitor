# sites_monitor
Python tool monitoring sites availability.
Sites can be configured using config.py stored in the same folder as sites_monitor.py script.
Tool includes a basic HTTP server showing webpages status. It is avaliable at localhost:8000 by default.

Check Interval an server port are configurable by passing ` and --port arguments to the commandline script.

# installation
- clone repo with `git clone <address>` (or manually copy and unpack zip or this repo)
- install with `python setup.py install`
- in case of issues with installing greenlet package (required by gevent), install gevent manually by `pip install gevent`

# usage
Run `python sites_monitor.py` to start the tool and the server.

To set the interval, pass --interval argument and value in seconds to the script, for example:
`python sites_monitor.py --interval 20` to check sites availability every 20 seconds.

To configure server's port, pass --port argument and port value to the script, for example:
`python sites_monitor.py --port 8899`
