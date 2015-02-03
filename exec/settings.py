import os

LANGS = {
    'python:2': {'ext': 'py',
                 'img': 'python:2',
                 'cmd':
                     lambda progname, ext, inputfile: 'python {}.{} < {}'.format(progname, ext, inputfile),
                 'compile': None},
    'python:3': {'ext': 'py',
                 'img': 'python:3',
                 'cmd':
                     lambda progname, ext, inputfile: 'python {}.{} < {}'.format(progname, ext, inputfile),
                 'compile': None},
    'c':        {'ext': 'c',
                 'img': 'gcc:4.9',
                 'cmd':
                     lambda progname, ext, inputfile: './a.out < {}'.format(inputfile),
                 'compile':
                     lambda inputfile, ext: 'gcc -O2 -W -Wall {}.{}'.format(inputfile, ext)},
    'c++':      {'ext': 'cpp',
                 'img': 'gcc:4.9',
                 'cmd':
                     lambda progname, ext, inputfile: './a.out < {}'.format(inputfile),
                 'compile':
                     lambda inputfile, ext: 'g++ -std=c++0x -O2 -W -Wall {}.{}'.format(inputfile, ext)},
    'java:7':   {'ext': 'java',
                 'img': 'java:7',
                 'cmd':
                     lambda progname, ext, inputfile: 'java -Xss10m {} < {}'.format(progname.title(), inputfile),
                 'compile':
                     lambda inputfile, ext: 'javac -Xlint {}.{}'.format(inputfile.title(), ext)},
    }

HOST_TESTDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'fixtures/testdata')
CONTAINER_TESTDATA_PATH = '/testdata'
