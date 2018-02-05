from setuptools import setup

setup(name='sites-monitor',
      version='1.0',
      description='Sites Monitor Tool with status webpage',
      author='Marcin Trzcinski',
      author_email='marcin.trzcinski@gmail.com',
      install_requires=['greenlet', 'gevent', 'requests'],
      )
