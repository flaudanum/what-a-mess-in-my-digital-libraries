# coding: UTF-8
"""
Unit tests for module 'compare'
Compatibility: python 3.X
"""

import unittest
import unittest.mock as um
import os
import sys
sys.path += ('../../whamdil',)
import subprocess
import shutil

from ptree   import *
from compare import *

class TestHandler(unittest.TestCase):


    def test_misnaming(self):
        """
        [REF]:
        Path_A/file_01
        [COMP]:
        Path_A/file_01_misnamed
        """

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        type(refPsObj).libFiles = um.PropertyMock(return_value=(refFile01Info,))
        type(refPsObj).directories = um.PropertyMock(return_value=({'id':1,'par':0,'name':'Path_A'},))
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId:'Path_A')
        refPsObj.matchHash = um.Mock(side_effect=lambda hashNum:refFile01Info)

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01_misnamed', 'dir':1,'hash':'00000000000000000000000000000000'}
        type(compPsObj).libFiles = um.PropertyMock(return_value=(compFile01Info,))
        type(compPsObj).directories = um.PropertyMock(return_value=({'id':1,'par':0,'name':'Path_A'},))
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId:'Path_A')
        compPsObj.matchHash = um.Mock(side_effect=lambda hashNum:compFile01Info)

        handlerObj = Handler(refPsObj, compPsObj)
        misnaming = handlerObj.misnaming[0]

        self.assertEqual(misnaming.refName, 'file_01')
        self.assertEqual(misnaming.compName, 'file_01_misnamed' )
        self.assertEqual(misnaming.path, 'Path_A')

        actionMessage = ['#MISNAMING: [REF]/Path_A/file_01\n',
                         'Rename file [COMP]/Path_A/file_01_misnamed\n']

        self.assertEqual(misnaming.action(), actionMessage)


    # def test_actions(self):
    #
    #     txtDescription = TestHandler.hdlObj.actions(view='txt')
    #
    #     with open('resources/test_compare.test_actions.txt','r') as buffRder:
    #         refDescription = buffRder.readlines()
    #
    #     self.assertEqual(refDescription,txtDescription)

if __name__=='__main__':

    unittest.main()
