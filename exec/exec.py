#------------------------------------------------------------------------------
# exec entrypoint
#------------------------------------------------------------------------------

import zipfile
import os
from docker import Client

#------------------------------------------------------------------------------

LANGS = {
    'python:2': {'ext': '.py',
                 'img': 'python:2',
                 'cmd': 'python'},
    'python:3': {'ext': '.py',
                 'img': 'python:3',
                 'cmd': 'python'},
    }

#------------------------------------------------------------------------------

def run_in_docker(archive_dir_name, progname, lang):
    '''
    Create docker container with volume dirname and run (python) program inside
    '''
    docker = Client(base_url='unix://var/run/docker.sock',
                    version='1.15')
    container = docker.create_container(
        image=LANGS[lang]['img'],
        volumes=['/tmp'],
        working_dir='/tmp',
        command='{} {}'.format(LANGS[lang]['cmd'], progname),
        network_disabled=True)
    response = docker.start(
        container.get('Id'),
        binds={archive_dir_name: {'bind': '/tmp', 'ro': True}})
    docker.wait(container.get('Id'))
    output = docker.logs(container.get('Id'))
    docker.stop(container.get('Id'))
    docker.remove_container(container.get('Id'))
    return output

#------------------------------------------------------------------------------

def run_task(userid, taskid, archive, lang):
    '''
    Runs user task stored in an archive written in given lang 
    '''
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    archive_path = os.path.join('testdata', 'user', userid, taskid, archive)
    with zipfile.ZipFile(archive_path) as zfile:
        for f in zfile.filelist:
            name, ext = os.path.splitext(f.filename)
            if ext == LANGS[lang]['ext']:
                zfile.extract(f.filename, 'tmp')
                return run_in_docker(os.path.abspath('tmp'), f.filename, lang)

#------------------------------------------------------------------------------
                
if __name__=='__main__':
    print(run_task('user1', 'lab1', 'lab.zip', 'python:3'))
