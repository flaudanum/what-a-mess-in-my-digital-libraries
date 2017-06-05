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


    def test_misnaming_01(self):
        """
        [REF]:
        Path_A/file_01
        [COMP]:
        Path_A/file_01_misnamed
        """

        #------------------------ B U I L D I N G   M O C K   O B J E C T S ------------------------

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        refLfPropertyMock = um.PropertyMock(return_value=(refFile01Info,))
        type(refPsObj).libFiles = refLfPropertyMock
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId:'Path_A')

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01_misnamed', 'dir':1,'hash':'00000000000000000000000000000000'}
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId:'Path_A')
        compPsObj.matchHash = um.Mock(side_effect=lambda hashNum: [compFile01Info,])

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        misnaming = handlerObj.misnaming[0]


        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        refPsObj.getRelPath.assert_called_once_with(1)
        refLfPropertyMock.assert_called_once_with()

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        compPsObj.getRelPath.assert_called_once_with(1)
        compPsObj.matchHash.assert_called_once_with('00000000000000000000000000000000')

        # Assertion on the properties of the 'compare.Misnaming' object
        self.assertEqual(misnaming.refName, 'file_01')
        self.assertEqual(misnaming.compName, 'file_01_misnamed' )
        self.assertEqual(misnaming.path, 'Path_A')

        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#MISNAMING: [REF]/Path_A/file_01\n',
                         'Rename file [COMP]/Path_A/file_01_misnamed\n']
        self.assertEqual(misnaming.action(), actionMessage)

    def test_misnaming_02(self):
        """
        [REF]:
        Path_A
        |_file_01
        file_01bis (=file_01)
        [COMP]:
        Path_A
        |_file_01_misnamed  (=file_01)
        file_01bis_misnamed (=file_01)
        """

        #------------------------ B U I L D I N G   M O C K   O B J E C T S ------------------------

        # Function definition for methods getRelPath() of Mock objects
        def getRelPath(dirId):
            pathsMap = {0:'', 1:'Path_A'}
            if dirId in pathsMap.keys():
                return pathsMap[dirId]
            else:
                raise ValueError('{0} not a proper dirId'.format(dirId))

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        refFile01bisInfo = {'name':'file_01bis', 'dir':0,'hash':'00000000000000000000000000000000'}
        refLfPropertyMock = um.PropertyMock(return_value=(refFile01Info,refFile01bisInfo))
        type(refPsObj).libFiles = refLfPropertyMock
        refPsObj.getRelPath = um.Mock(side_effect=getRelPath)

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01_misnamed', 'dir':1,'hash':'00000000000000000000000000000000'}
        compFile01bisInfo = {'name':'file_01bis_misnamed', 'dir':0,'hash':'00000000000000000000000000000000'}
        compPsObj.getRelPath = um.Mock(side_effect=getRelPath)
        compPsObj.matchHash = um.Mock(side_effect=lambda hashNum: [compFile01Info,compFile01bisInfo])

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        misnaming = sorted(handlerObj.misnaming, key=(lambda m: m.refName))

        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        calls = [um.call(0), um.call(1)]
        refPsObj.getRelPath.assert_has_calls(calls, any_order=True)
        refLfPropertyMock.assert_called_with()

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        compPsObj.getRelPath.assert_has_calls(calls, any_order=True)
        compPsObj.matchHash.assert_called_with('00000000000000000000000000000000')

        # Assertion on the properties of the 'compare.Misnaming' object
        self.assertEqual(misnaming[0].refName, 'file_01')
        self.assertEqual(misnaming[0].compName, 'file_01_misnamed' )
        self.assertEqual(misnaming[0].path, 'Path_A')

        self.assertEqual(misnaming[1].refName, 'file_01bis')
        self.assertEqual(misnaming[1].compName, 'file_01bis_misnamed' )
        self.assertEqual(misnaming[1].path, '')

        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#MISNAMING: [REF]/Path_A/file_01\n',
                         'Rename file [COMP]/Path_A/file_01_misnamed\n']
        self.assertEqual(misnaming[0].action(), actionMessage)
        actionMessage = ['#MISNAMING: [REF]/file_01bis\n',
                         'Rename file [COMP]/file_01bis_misnamed\n']
        self.assertEqual(misnaming[1].action(), actionMessage)

        # Testing output of method compare.Misnaming.shell()
        shellCommands = ['mv $COMP/Path_A/file_01_misnamed $COMP/Path_A/file_01\n',]
        self.assertEqual(misnaming[0].shell(), shellCommands)
        shellCommands = ['mv $COMP/file_01bis_misnamed $COMP/file_01bis\n',]
        self.assertEqual(misnaming[1].shell(), shellCommands)




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
