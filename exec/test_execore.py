#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# test_execore.py
#------------------------------------------------------------------------------

import unittest
import execore

#------------------------------------------------------------------------------

class TestExecoreMalformed(unittest.TestCase):

    def test_nonexisting_dir(self):
        with self.assertRaises(Exception):
            execore.Exec(testdata_path='fixtures/invalid/nonexisting')

    def test_empty_dir(self):
        with self.assertRaises(Exception):
            execore.Exec(testdata_path='fixtures/invalid/empty')

    def test_nocfg(self):
        with self.assertRaises(Exception):
            execore.Exec(testdata_path='fixtures/invalid/nocfg/testdata')

#------------------------------------------------------------------------------

class TestExecore(unittest.TestCase):
    
    def setUp(self):
        self._exec = execore.Exec(testdata_path='fixtures/testdata')

    def test_get_registered_tasks(self):
        self.assertEqual(self._exec.get_registered_tasks(), ['task1'])

    # Base tests
    def run_integration_(self, task, user, archive, lang):
        result = self._exec.run(task, user, archive, lang, integration=True)
        self.assertEqual(result['passed'], True)

    def run_(self, task, user, archive, lang):
        result = self._exec.run(task, user, archive, lang)
        self.assertEqual(len(result), 4)
        for r in result:
            if r['name'].endswith('_fail'):
                self.assertEqual(r['passed'], False)
            else:
                self.assertEqual(r['passed'], True)

    # Compile error
    def test_compile_error(self):
        result = self._exec.run('task1', 'user_compile_err', 'Sum.zip',
                                'java:7', True)
        self.assertEqual(result['passed'], False)
        self.assertGreater(result['result'][0]['COMPILE'].find('error'), -1)

    # Python tests
    def test_run_integration_python(self):
        self.run_integration_('task1', 'user1', 'sum.zip', 'python:3')

    def test_run_python(self):
        self.run_('task1', 'user1', 'sum.zip', 'python:3')

    # C tests
    def test_run_integration_c(self):
        self.run_integration_('task1', 'user2', 'sum.zip', 'c')

    def test_run_c(self):
        self.run_('task1', 'user2', 'sum.zip', 'c')

    # C++ tests
    def test_run_integration_c(self):
        self.run_integration_('task1', 'user3', 'sum.zip', 'c++')

    def test_run_c(self):
        self.run_('task1', 'user3', 'sum.zip', 'c++')

    # Java tests
    def test_run_integration_java(self):
        self.run_integration_('task1', 'user4', 'Sum.zip', 'java:7')

    def test_run_java(self):
        self.run_('task1', 'user4', 'Sum.zip', 'java:7')

#------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
