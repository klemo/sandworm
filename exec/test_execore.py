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

    # Python tests
    def test_run_integration_python(self):
        result = self._exec.run('task1', 'user1', 'sum.zip', 'python:3',
                                integration=True)
        self.assertEqual(result['passed'], True)

    def test_run_python(self):
        result = self._exec.run('task1', 'user1', 'sum.zip', 'python:3')
        self.assertEqual(len(result), 4)
        for r in result:
            if r['name'].endswith('_fail'):
                self.assertEqual(r['passed'], False)
            else:
                self.assertEqual(r['passed'], True)

    # C tests
    def test_run_integration_c(self):
        result = self._exec.run('task1', 'user2', 'sum.zip', 'c',
                                integration=True)
        self.assertEqual(result['passed'], True)

    def test_run_c(self):
        result = self._exec.run('task1', 'user2', 'sum.zip', 'c')
        self.assertEqual(len(result), 4)
        for r in result:
            if r['name'].endswith('_fail'):
                self.assertEqual(r['passed'], False)
            else:
                self.assertEqual(r['passed'], True)

    # C++ tests
    def test_run_integration_c(self):
        result = self._exec.run('task1', 'user3', 'sum.zip', 'c++',
                                integration=True)
        self.assertEqual(result['passed'], True)

    def test_run_c(self):
        result = self._exec.run('task1', 'user3', 'sum.zip', 'c++')
        self.assertEqual(len(result), 4)
        for r in result:
            if r['name'].endswith('_fail'):
                self.assertEqual(r['passed'], False)
            else:
                self.assertEqual(r['passed'], True)

#------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
