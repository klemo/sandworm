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
                                  'testdata')
HOST_TESTDATA_TASKS = os.path.join(HOST_TESTDATA_PATH, 'labs')
CONTAINER_TESTDATA_PATH = '/testdata'
