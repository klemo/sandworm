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

    def test_run(self):
        result = self._exec.run('task1', 'user1', 'sum.zip', 'python:3')
        self.assertEqual(len(result), 3)

#------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
