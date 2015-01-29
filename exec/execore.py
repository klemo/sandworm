#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# exec entrypoint
#------------------------------------------------------------------------------

import zipfile
import os
import docker
import settings
import logging.config
import yaml
import pprint

#------------------------------------------------------------------------------
class TestRunner():
    '''
    Encapsulates functionalities for handling tests for single task.
    '''

    #-------------------------------------------------------------------------- 
    def __init__(self, taskid):
        self.taskid = taskid # task to evaluate
        self.logger = logging.getLogger('debug.{}.{}'.format(
                self.__class__.__name__,
                taskid))
        # locate testdata for given task
        self.testdata_archive_path = os.path.join(settings.HOST_TESTDATA_PATH,
                                                  'labs',
                                                  self.taskid)
        self.cfg = []
        self.analyze_testdata()
        
    #--------------------------------------------------------------------------
    def analyze_testdata(self):
        '''
        Analyzes and parses tests from the testdata folder
        '''
        self.logger.info('// Checking task folder: {}'.format(
                self.testdata_archive_path))
        if not os.path.isdir(self.testdata_archive_path):
            raise Exception('Not a directory: {}'.format(
                    self.testdata_archive_path))
        self.read_cfg()
        # parse tests
        self.tests = []
        for test_name in os.listdir(self.testdata_archive_path):
            test_dir = os.path.join(self.testdata_archive_path, test_name)
            if os.path.isdir(test_dir):
                # parse .in and .out files
                iofiles = os.listdir(test_dir)
                if iofiles:
                    test = {'name': test_name,
                            'in': None,
                            'out': None}
                    for iofile in os.listdir(test_dir):
                        name, ext = os.path.splitext(iofile)
                        test[ext[1:]] = iofile
                    self.tests.append(test)
                else:
                    self.logger.info('Ignoring empty folder: {}'.format(
                            test_name))
        if self.tests:
            self.logger.info('Found tests: OK ({} tests)'.format(
                    len(self.tests)))
            integration_test = None
            for test in self.tests:
                if test['name'] == 'integration':
                    integration_test = test
                    self.logger.info('Integration test: OK')
                    self.tests.remove(integration_test)
                    break
            if not integration_test:
                raise Exception('Integration test: Not found')
        
    #--------------------------------------------------------------------------
    def read_cfg(self):
        '''
        Read configuration file and store commands in self.cfg
        '''
        cfg_path = self.testdata_archive_path + '/eval.cfg'
        try:
            with open(cfg_path, 'r') as cfg_file:
                self.logger.info('Config file: OK')
                for line in cfg_file:
                    # get rid of comments and surrounding whitespace
                    line = line.split('#')[0].strip()
                    if len(line) > 0: # don't want empty lines
                        self.cfg.append(line)
        except Exception as e:
            raise Exception('Config file: {}'.format(e))
        if not self.cfg:
            raise Exception('Empty config file!')
                    
    #--------------------------------------------------------------------------
    def run_in_docker(self, user_archive, progname, input_file, lang):
        '''
        Create docker container with volume dirname and run (python) program
        inside
        '''
        main_cmd = '{} {}.{} < {}'.format(settings.LANGS[lang]['cmd'],
                                          progname,
                                          settings.LANGS[lang]['ext'],
                                          input_file)
        dckr = docker.Client(base_url='unix://var/run/docker.sock',
                             version='1.15')
        container = dckr.create_container(
            image=settings.LANGS[lang]['img'],
            volumes=['/tmp', settings.CONTAINER_TESTDATA_PATH],
            working_dir='/tmp',
            command='/bin/bash -c "{}"'.format(main_cmd),
            network_disabled=True)
        response = dckr.start(
            container.get('Id'),
            binds={user_archive: {'bind': '/tmp'},
                   self.testdata_archive_path: {
                    'bind': settings.CONTAINER_TESTDATA_PATH,
                    'ro': True}})
        dckr.wait(container.get('Id'))
        dckr.stop(container.get('Id'))
        output = dckr.logs(container.get('Id'))
        dckr.remove_container(container.get('Id'))
        return output

    #--------------------------------------------------------------------------
    def eval_cfg(self, test, lang):
        '''
        Evaluates commands from the configuration file for self.taskid and runs
        single test written in lang
        '''
        self.logger.info('// Test: {}'.format(test['name']))
        passed = True
        result = []
        last_result = None
        try:
            for line in self.cfg:
                self.logger.info('Running command ' + line)
                cmd_result = {}
                parts = line.split()
                option = parts[0]
                # CWD
                if option.upper() == 'CWD':
                    cmd_result[option] = None
                    pass
                # COMPILE
                elif option.upper() == 'COMPILE':
                    cmd_result[option] = None
                    pass
                # RUN
                elif option.upper() == 'RUN':
                    what = parts[1]
                    timeout = int(parts[2])
                    input_filename = None
                    if len(parts) == 4:
                        input_filename = os.path.join(
                            settings.CONTAINER_TESTDATA_PATH,
                            test['name'],
                            test[parts[3]])
                        last_result = self.run_in_docker(
                            os.path.abspath('tmp'),
                            what,
                            input_filename,
                            lang)
                    cmd_result[option] = last_result
                # ASSERT
                elif option.upper() == 'ASSERT':
                    # read expected output
                    output_filename = os.path.join(
                        self.testdata_archive_path,
                        test['name'],
                        test[parts[1]])
                    with open(output_filename, 'r') as fout:
                        expected = fout.read()
                        # and check for equality
                        if last_result.strip() != expected.strip():
                            self.logger.info('Passed: False')
                            self.logger.info('Expected:\n{}\nGot:\n{}\n'.format(
                                    expected,
                                    last_result))
                            passed = False
                            cmd_result[option] = {
                                'assert': False,
                                'expected': expected,
                                'got': last_result}
                        else:
                            self.logger.info('Passed: True')
                            cmd_result[option] = {'assert': True}
                # append result of every command
                result.append(cmd_result)
        except Exception as e:
            self.logger.error('eval_cfg:', exc_info=True)
            passed = False
        return result

    #--------------------------------------------------------------------------
    def eval_all(self, lang):
        '''
        Short for evaluation of all tests
        '''
        return [self.eval_cfg(test, lang) for test in self.tests]
        
    #--------------------------------------------------------------------------
    def run(self, userid, archive, lang, only_integration=False):
        '''
        Runs user task stored in an archive written in given lang with an
        option for running only integration test
        '''
        self.logger.info('// Running tests for user {}'.format(userid))
        wdir = 'tmp'
        if not os.path.exists(wdir):
            os.makedirs(wdir)
        user_archive_path = os.path.join(settings.HOST_TESTDATA_PATH,
                                         'user',
                                         userid,
                                         self.taskid,
                                         archive)
        try:
            with zipfile.ZipFile(user_archive_path) as zfile:
                zfile.extractall(path=wdir)
                self.logger.info('Extracting user archive: OK')
        except Exception as e:
            raise Exception('Extracting user archive: {}'.format(e))
        if only_integration:
            return [self.eval_cfg('integration', lang)]
        else:
            return self.eval_all(lang)

#------------------------------------------------------------------------------
class Exec():
    '''
    Main EXEC entry point. By default, locates task folders in
    settings.HOST_TESTDATA_PATH and registers them. Use run function to run
    tests for user's archive.
    '''

    #--------------------------------------------------------------------------
    def __init__(self, testdata_path=None):
        '''
        testdata_path is the location of the test folders for each task
        '''
        self.logger = logging.getLogger('debug.{}'.format(
                self.__class__.__name__))
        if not testdata_path:
            testdata_path = settings.HOST_TESTDATA_TASKS
        self.testdata_path = testdata_path
        self.logger.info('// Checking testdata folder: {}'.format(
                self.testdata_path))
        if not os.path.isdir(self.testdata_path):
            raise Exception('TESTDATA_PATH not a directory: {}'.format(
                    self.testdata_path))
        self.test_runners = {}
        for task_name in os.listdir(self.testdata_path):
            self.logger.info('Found task: {}'.format(task_name))
            try:
                self.test_runners[task_name] = TestRunner(task_name)
            except Exception as e:
                self.logger.info(
                    'Registering test runner for {} failed: {}'.format(
                        task_name, e))

    #--------------------------------------------------------------------------
    def get_registered_tasks(self):
        '''
        Returns list of registered tasks
        '''
        return self.test_runners.keys()

    #--------------------------------------------------------------------------
    def run(self, taskid, userid, archive, lang, only_integration=False):
        '''
        Runs single task for given user archive written in lang with an
        option for running only integration test
        '''
        test_runner = self.test_runners.get(taskid)
        if test_runner:
            return test_runner.run(userid, archive, lang)
        else:
            self.logger.info('Task runner for {} not registered'.format(
                    taskid))

#------------------------------------------------------------------------------
if __name__=='__main__':
    with open('logging.yml', 'r') as f:
        config_dict = yaml.load(f)
        logging.config.dictConfig(config_dict)
        exec_ = Exec()
        #pprint.pprint(exec_.run('lab1', 'user1', 'lab.zip', 'python:3'))