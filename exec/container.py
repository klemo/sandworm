#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# container (docker) services
#------------------------------------------------------------------------------

import os
import docker
import settings
import logging

#------------------------------------------------------------------------------
class Container():
    '''
    Encapsulates functionalities for handling sandboxing in containers
    '''

    #--------------------------------------------------------------------------
    def __init__(self, testdata_archive_path, user_archive, lang):
        self.logger = logging.getLogger('debug.docker')
        self.testdata_archive_path = testdata_archive_path
        self.user_archive = user_archive
        self.lang = lang
        self.dckr = docker.Client(base_url='unix://var/run/docker.sock',
                                  version='1.15')
        
    #--------------------------------------------------------------------------
    def create(self, cmd, timeout):
        '''
        Creates container for every command. Should refactor this to use
        EXECUTE command... Also, writes to volume -- should use COMMIT
        instead.
        '''
        self.container = self.dckr.create_container(
            image=settings.LANGS[self.lang]['img'],
            volumes=['/tmp', settings.CONTAINER_TESTDATA_PATH],
            working_dir='/tmp',
            command='/bin/bash -c "{}"'.format(cmd),
            network_disabled=True,
            detach=True)
        cid = self.container.get('Id')
        resp = self.dckr.start(
            cid,
            binds={self.user_archive: {'bind': '/tmp'},
                   self.testdata_archive_path: {
                    'bind': settings.CONTAINER_TESTDATA_PATH, 'ro': True}})
        # resp = self.dckr.execute(cid,
        #                          cmd='/bin/bash -c "{}"'.format(main_cmd))
        self.dckr.wait(cid, timeout=timeout)
        self.dckr.stop(cid)
        stdout = self.dckr.logs(cid, stdout=True, stderr=False)
        stderr = self.dckr.logs(cid, stdout=False, stderr=True)
        return stdout.strip(), stderr.strip()

    #--------------------------------------------------------------------------
    def remove(self):
        self.dckr.remove_container(self.container.get('Id'))

    #--------------------------------------------------------------------------
    def cmd_run(self, progname, input_file, timeout=None):
        '''
        RUN command
        '''
        cmd = settings.LANGS[self.lang]['cmd'](progname,
                                               settings.LANGS[self.lang]['ext'],
                                               input_file)
        output = self.create(cmd, timeout)
        self.remove()
        return output

    #--------------------------------------------------------------------------
    def cmd_compile(self, input_file, timeout=None):
        '''
        COMPILE command
        '''
        compile_cmd = settings.LANGS[self.lang].get('compile')
        if compile_cmd:
            cmd = compile_cmd(input_file,
                              settings.LANGS[self.lang]['ext'])
            output = self.create(cmd, timeout)
            self.remove()
            return output
        return (None, None)
