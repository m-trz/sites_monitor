"""
Configuration file containing sites settings
(address, text-to-check pairs)
"""

sites = (
    ('http://google.pl', 'Szukaj'),
    ('http://wired.com', 'business'),
    ('http://foobar.com/test', 'spam'),
    ('http://httpstat.us/204', 'Log in'),
    ('http://httpstat.us/401', 'Text'),
    ('http://httpstat.us/408', 'timeout'),
    ('https://www.python.org/', 'Success Stories'),
    ('https://github.com/requests/requests/', 'Pull requests'),
    ('https://github.com/', 'not existing text'),
    ('http://not-existing-web-page.com', 'some text')
)
