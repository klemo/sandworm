#------------------------------------------------------------------------------
# exec entrypoint
#------------------------------------------------------------------------------

import zipfile
import os
import logging
from docker import Client

#------------------------------------------------------------------------------

LANGS = {
    'python:2': {'ext': 'py',
                 'img': 'python:2',
                 'cmd': 'python'},
    'python:3': {'ext': 'py',
                 'img': 'python:3',
                 'cmd': 'python'},
    }

#------------------------------------------------------------------------------

def run_in_docker(testdata_archive, user_archive, progname, input_file, lang):
    '''
    Create docker container with volume dirname and run (python) program inside
    '''
    main_cmd = '{} {}.{} < {}'.format(LANGS[lang]['cmd'],
                                      progname,
                                      LANGS[lang]['ext'],
                                      input_file)
    docker = Client(base_url='unix://var/run/docker.sock',
                    version='1.15')
    container = docker.create_container(
        image=LANGS[lang]['img'],
        volumes=['/tmp', '/testdata'],
        working_dir='/tmp',
        command='/bin/bash -c "{}"'.format(main_cmd),
        network_disabled=True)
    response = docker.start(
        container.get('Id'),
        binds={user_archive: {'bind': '/tmp'},
               testdata_archive: {'bind': '/testdata', 'ro': True}})
    docker.wait(container.get('Id'))
    docker.stop(container.get('Id'))
    output = docker.logs(container.get('Id'))
    docker.remove_container(container.get('Id'))
    return output

#------------------------------------------------------------------------------

def eval_cfg(taskid, test_name, lang):
    '''
    Evaluates configuration file for task taskid and runs test_name written in
    lang
    '''
    passed = False
    testdata_archive_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'testdata',
        'labs',
        taskid)
    cfg = []
    with open(testdata_archive_path + '/eval.cfg', 'r') as cfg_file:
        for line in cfg_file:
            # get rid of comments and surrounding whitespace
            line = line.split('#')[0].strip()
            if len(line) > 0: # don't want empty lines
                cfg.append(line)
    try:
        for line in cfg:
            logging.info('running command ' + line)
            parts = line.split()
            option = parts[0]
            if option == 'cwd':
                pass
            elif option == 'compile':
                pass
            elif option == 'run':
                what = parts[1]
                timeout = int(parts[2])
                input_filename = None
                if len(parts) == 4:
                    input_filename = '/testdata/{}/primjer.{}'.format(test_name, parts[3])

                out = run_in_docker(testdata_archive_path,
                                    os.path.abspath('tmp'),
                                    what,
                                    input_filename,
                                    lang)
                print(out)

            elif option == 'check_output':
                pass
            elif option == 'FRISCjs':
                pass
    except Exception as e:
        logging.error('eval_cfg: {}'.format(e))
        passed = False

#------------------------------------------------------------------------------

def run_task(userid, taskid, archive, lang, check_integration=True):
    '''
    Runs user task stored in an archive written in given lang 
    '''
    wdir = 'tmp'
    if not os.path.exists(wdir):
        os.makedirs(wdir)
    user_archive_path = os.path.join('testdata',
                                     'user',
                                     userid,
                                     taskid,
                                     archive)
    with zipfile.ZipFile(user_archive_path) as zfile:
        zfile.extractall(path=wdir)
    if check_integration:
        eval_cfg(taskid, 'integration', lang)

#------------------------------------------------------------------------------
                
if __name__=='__main__':
    run_task('user1', 'lab1', 'lab.zip', 'python:3')
