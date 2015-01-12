#------------------------------------------------------------------------------
# exec entrypoint
#------------------------------------------------------------------------------

import zipfile
import os
from docker import Client

#------------------------------------------------------------------------------

def run_in_docker(dirname, progname):
    '''
    Create docker container with volume dirname and run (python) program inside
    '''
    docker = Client(base_url='unix://var/run/docker.sock',
                    version='1.15')
    container = docker.create_container(image='python:2',
                                        volumes={'/tmp':''},
                                        working_dir='/tmp',
                                        command='python {}'.format(progname),
                                        network_disabled=True)
    response = docker.start(container.get('Id'),
                            binds={dirname: {'bind': '/tmp'}})
    docker.wait(container.get('Id'))
    output = docker.logs(container.get('Id'))
    docker.stop(container.get('Id'))
    docker.remove_container(container.get('Id'))
    return output

#------------------------------------------------------------------------------

def run_job(filename):
    '''
    Runs job stored in an archive
    '''
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    with zipfile.ZipFile(filename) as zfile:
        for f in zfile.filelist:
            name, ext = os.path.splitext(f.filename)
            if ext == '.py':
                zfile.extract(f.filename, 'tmp')
                return run_in_docker(os.path.abspath('tmp'), f.filename)

#------------------------------------------------------------------------------
                
if __name__=='__main__':
    print(run_job('p1.zip'))
