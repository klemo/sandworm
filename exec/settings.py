import os

LANGS = {
    'python:2': {'ext': 'py',
                 'img': 'python:2',
                 'cmd': 'python'},
    'python:3': {'ext': 'py',
                 'img': 'python:3',
                 'cmd': 'python'},
    }

HOST_TESTDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'fixtures/testdata')
CONTAINER_TESTDATA_PATH = '/testdata'
