#------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# test_execore.py
#------------------------------------------------------------------------------

import unittest
import execore

#------------------------------------------------------------------------------

class TestExecore(unittest.TestCase):
    
    def setUp(self):
        self._exec = execore.Exec()

    def test_get_registered_tasks(self):
        self.assertEqual(self._exec.get_registered_tasks(), ['lab1'])

    def test_run(self):
        result = self._exec.run('lab1', 'user1', 'lab.zip', 'python:3')
        self.assertEqual(len(result), 30)

#------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
