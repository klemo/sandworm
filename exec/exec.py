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

class TestRunner():

    #-------------------------------------------------------------------------- 
    def __init__(self, taskid):
        self.taskid = taskid # task to evaluate
        # locate testdata for given task
        self.testdata_archive_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'testdata', 'labs',
            self.taskid)
        self.cfg = []
        self.read_cfg()
        
    #--------------------------------------------------------------------------
    def read_cfg(self):
        '''
        Read configuration file and store commands in self.cfg
        '''
        try:
            with open(self.testdata_archive_path + '/eval.cfg', 'r') as cfg_file:
                for line in cfg_file:
                    # get rid of comments and surrounding whitespace
                    line = line.split('#')[0].strip()
                    if len(line) > 0: # don't want empty lines
                        self.cfg.append(line)
        except Exception as e:
            raise Exception('read_cfg: {}'.format(e))
                    
    #--------------------------------------------------------------------------
    def run_in_docker(self, user_archive, progname, input_file, lang):
        '''
        Create docker container with volume dirname and run (python) program
        inside
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
                   self.testdata_archive_path: {'bind': '/testdata',
                                                'ro': True}})
        docker.wait(container.get('Id'))
        docker.stop(container.get('Id'))
        output = docker.logs(container.get('Id'))
        docker.remove_container(container.get('Id'))
        return output

    #--------------------------------------------------------------------------
    def eval_cfg(self, test_name, lang):
        '''
        Evaluates configuration file for self.taskid and runs test_name
        written in lang
        '''
        passed = True
        last_result = None
        try:
            for line in self.cfg:
                logging.info('Running command ' + line)
                parts = line.split()
                option = parts[0]
                # CWD
                if option.upper() == 'CWD':
                    pass
                # COMPILE
                elif option.upper() == 'COMPILE':
                    pass
                # RUN
                elif option.upper() == 'RUN':
                    what = parts[1]
                    timeout = int(parts[2])
                    input_filename = None
                    if len(parts) == 4:
                        input_filename = '/testdata/{}/primjer.{}'.format(
                            test_name, parts[3])

                        last_result = self.run_in_docker(
                            os.path.abspath('tmp'),
                            what,
                            input_filename,
                            lang)
                # ASSERT
                elif option.upper() == 'ASSERT':
                    # read expected output
                    output_filename = os.path.join(
                        self.testdata_archive_path,
                        test_name,
                        'primjer.{}'.format(parts[1]))
                    with open(output_filename, 'r') as fout:
                        expected = fout.read()
                        # and check for equality
                        if last_result.strip() != expected.strip():
                            print('Expected:\n{}\nGot:\n{}\n'.format(
                                    expected,
                                    last_result))
                            passed = False
                        else:
                            logging.info('Test passed!')
        except Exception as e:
            logging.error('eval_cfg: {}'.format(e))
            passed = False

    #--------------------------------------------------------------------------
    def run(self, userid, archive, lang, check_integration=True):
        '''
        Runs user task stored in an archive written in given lang 
        '''
        wdir = 'tmp'
        if not os.path.exists(wdir):
            os.makedirs(wdir)
        user_archive_path = os.path.join('testdata',
                                         'user',
                                         userid,
                                         self.taskid,
                                         archive)
        try:
            with zipfile.ZipFile(user_archive_path) as zfile:
                zfile.extractall(path=wdir)
        except Exception as e:
            raise Exception(e)
        if check_integration:
            self.eval_cfg('integration', lang)

#------------------------------------------------------------------------------
                
if __name__=='__main__':
    logging.getLogger('').handlers = []
    logging.basicConfig(level=getattr(logging, 'DEBUG', None),
                        format='%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.getLogger('docker').setLevel(logging.CRITICAL)
    taskid = 'lab1'
    tr = TestRunner(taskid)
    tr.run('user1', 'lab.zip', 'python:3')
