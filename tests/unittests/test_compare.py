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


    def getRelPath(self, dirId, pathsMap):
        """
        Surrogate function for method PathScan.getRelPath()
        """
        if dirId in pathsMap.keys():
            return pathsMap[dirId]
        else:
            raise ValueError('{0} not a proper dirId'.format(dirId))

    def matchHash(self, hashNum, hashDict):
        """
        Surrogate function for method PathScan.matchHash()
        """
        if hashNum in hashDict.keys():
            return hashDict[hashNum]
        else:
            return []


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
        type(compPsObj).libFiles = um.PropertyMock(return_value=None) # unused --> the 'new files' detection

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        misnaming = handlerObj.misnaming[0]


        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        refPsObj.getRelPath.assert_called_with(1)
        refLfPropertyMock.assert_called_once_with()

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        compPsObj.getRelPath.assert_called_with(1)
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

        # # Function definition for methods getRelPath() of Mock objects
        # def getRelPath(dirId):
        #     pathsMap = {0:'', 1:'Path_A'}
        #     if dirId in pathsMap.keys():
        #         return pathsMap[dirId]
        #     else:
        #         raise ValueError('{0} not a proper dirId'.format(dirId))

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        refFile01bisInfo = {'name':'file_01bis', 'dir':0,'hash':'00000000000000000000000000000000'}
        refLfPropertyMock = um.PropertyMock(return_value=(refFile01Info,refFile01bisInfo))
        type(refPsObj).libFiles = refLfPropertyMock
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A'}))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01_misnamed', 'dir':1,'hash':'00000000000000000000000000000000'}
        compFile01bisInfo = {'name':'file_01bis_misnamed', 'dir':0,'hash':'00000000000000000000000000000000'}
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A'}))
        compPsObj.matchHash = um.Mock(side_effect=lambda hashNum: [compFile01Info,compFile01bisInfo])
        type(compPsObj).libFiles = um.PropertyMock(return_value=None) # unused --> the 'new files' detection

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
        shellCommands = ['# Misnaming $REF/Path_A/file_01\n',
        'mv $COMP/Path_A/file_01_misnamed $COMP/Path_A/file_01\n',]
        self.assertEqual(misnaming[0].shell(), shellCommands)
        shellCommands = ['# Misnaming $REF/file_01bis\n',
        'mv $COMP/file_01bis_misnamed $COMP/file_01bis\n',]
        self.assertEqual(misnaming[1].shell(), shellCommands)


    def test_misplacement(self):
        """
        [REF]:
        Path_A
        |_file_01
        Path_B
        |_file_01bis (=file_01)
        file_02
        [COMP]:
        Path_C
        |_file_01
        Path_D
        |_file_01bis_misnamed (=file_01)
        file_02

        Output from method action():

        # MISPLACEMENT: [REF]/Path_A/file_01
        Move file [COMP]/Path_C/file_01 to [COMP]/Path_A/file_01
        Remove file [COMP]/Path_D/file_01bis_misnamed

        # MISPLACEMENT: [REF]/Path_B/file_01bis
        Move file [COMP]/Path_C/file_01 to [COMP]/Path_B/file_01bis
        Remove file [COMP]/Path_D/file_01bis_misnamed

        Output from method shell():

        # MISPLACEMENT: [REF]/Path_A/file_01
        mv -i $COMP/Path_C/file_01 to $COMP/Path_A/file_01
        rm $COMP/Path_D/file_01bis_misnamed

        # MISPLACEMENT: [REF]/Path_B/file_01bis
        mv -i $COMP/Path_C/file_01 to $COMP/Path_B/file_01bis
        rm $COMP/Path_D/file_01bis_misnamed
        """

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        refFile01bisInfo = {'name':'file_01bis', 'dir':2,'hash':'00000000000000000000000000000000'}
        refFile02Info = {'name':'file_02', 'dir':0,'hash':'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'}
        refLfPropertyMock = um.PropertyMock(return_value=[refFile01Info,refFile01bisInfo,refFile02Info])
        type(refPsObj).libFiles = refLfPropertyMock
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        compFile01bisInfo = {'name':'file_01bis_misnamed', 'dir':2,'hash':'00000000000000000000000000000000'}
        compFile02Info = {'name':'file_02', 'dir':0,'hash':'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'}
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_C',2:'Path_D'}))
        hdict = {\
        '00000000000000000000000000000000':[compFile01Info,compFile01bisInfo],
        'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF':[compFile02Info,]}
        compPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=hdict))
        type(compPsObj).libFiles = um.PropertyMock(return_value=None) # unused --> the 'new files' detection


        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        misplacements = sorted(handlerObj.misplacement, key=(lambda m: m.refName))

        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        getRelPathCalls = [um.call(0), um.call(1), um.call(2)]
        refPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)
        refLfPropertyMock.assert_called_with()

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        compPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)
        matchHashCalls = [um.call('00000000000000000000000000000000'), um.call('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')]
        compPsObj.matchHash.assert_has_calls(matchHashCalls, any_order=True)
        self.assertEqual(compPsObj.matchHash.call_count,3)

        # Assertion on the properties of the 'compare.Misnaming' object
        self.assertEqual(len(misplacements),2)

        self.assertEqual(misplacements[0].refName, 'file_01')
        self.assertEqual(misplacements[0].refPath, 'Path_A')
        self.assertEqual(misplacements[0].compFounds, [('Path_C','file_01'),('Path_D','file_01bis_misnamed')])

        self.assertEqual(misplacements[1].refName, 'file_01bis')
        self.assertEqual(misplacements[1].refPath, 'Path_B')
        self.assertEqual(misplacements[1].compFounds, [('Path_C','file_01'),('Path_D','file_01bis_misnamed')])


        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#MISPLACEMENT: [REF]/Path_A/file_01\n',
                         'Move file [COMP]/Path_C/file_01 to [COMP]/Path_A/file_01\n',
                         'Remove file [COMP]/Path_D/file_01bis_misnamed\n']
        self.assertEqual(misplacements[0].action(), actionMessage)
        actionMessage = ['#MISPLACEMENT: [REF]/Path_B/file_01bis\n',
                         'Move file [COMP]/Path_C/file_01 to [COMP]/Path_B/file_01bis\n',
                         'Remove file [COMP]/Path_D/file_01bis_misnamed\n']
        self.assertEqual(misplacements[1].action(), actionMessage)


        # Testing output of method compare.Misnaming.shell()
        shellCommands = ['# Misplaced copies of [REF]/Path_A/file_01\n',
        'mv $COMP/Path_C/file_01 $COMP/Path_A/file_01\n',
        'rm -i $COMP/Path_D/file_01bis_misnamed\n']
        self.assertEqual(misplacements[0].shell(), shellCommands)
        shellCommands = ['# Misplaced copies of [REF]/Path_B/file_01bis\n',
        'mv $COMP/Path_C/file_01 $COMP/Path_B/file_01bis\n',
        'rm -i $COMP/Path_D/file_01bis_misnamed\n']
        self.assertEqual(misplacements[1].shell(), shellCommands)

    def test_describeText_01(self):


        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        refFile01bisInfo = {'name':'file_01bis', 'dir':2,'hash':'00000000000000000000000000000000'}
        refLfPropertyMock = um.PropertyMock(return_value=(refFile01Info,refFile01bisInfo))
        type(refPsObj).libFiles = refLfPropertyMock
        type(refPsObj).path = um.PropertyMock(return_value='Return from property path of Mock object named \'mock_refPathScan\'')
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{1:'Path_A',2:'Path_B'}))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFile01Info = {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'}
        compFile01bisInfo = {'name':'file_01bis_misnamed', 'dir':2,'hash':'00000000000000000000000000000000'}
        type(compPsObj).path = um.PropertyMock(return_value='Return from property path of Mock object named \'mock_compPathScan\'')
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{1:'Path_C',2:'Path_D'}))
        hdict = {\
        '00000000000000000000000000000000':[compFile01Info,compFile01bisInfo],}
        compPsObj.matchHash = um.Mock(side_effect=lambda num: self.matchHash(hashNum=num, hashDict=hdict))
        type(compPsObj).libFiles = um.PropertyMock(return_value=None) # unused --> the 'new files' detection

        # compPsObj.matchHash = um.Mock(side_effect=lambda hashNum: [compFile01Info,compFile01bisInfo])

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        handlerObj.describe()

        #----------------------------------- A S S E R T I O N S -----------------------------------

        filepath='./whamdil.log'
        with open(filepath,'r') as buffRder:
            logText = list(buffRder)

        refLogText=[\
        '[REF]: Return from property path of Mock object named \'mock_refPathScan\'\n',
        '[COMP]: Return from property path of Mock object named \'mock_compPathScan\'\n',
        '\n',
        '#MISPLACEMENT: [REF]/Path_A/file_01\n',
        'Move file [COMP]/Path_C/file_01 to [COMP]/Path_A/file_01\n',
        'Remove file [COMP]/Path_D/file_01bis_misnamed\n',
        '\n',
        '#MISPLACEMENT: [REF]/Path_B/file_01bis\n',
        'Move file [COMP]/Path_C/file_01 to [COMP]/Path_B/file_01bis\n',
        'Remove file [COMP]/Path_D/file_01bis_misnamed\n',
        '\n']
        for ref,comp in zip(refLogText,logText):
            self.assertEqual(ref,comp)
        self.assertEqual(refLogText,logText)

        os.unlink(filepath)

    def test_missing(self):
        """
        [REF]:
        Path_A
        |_file_01
        Path_B
        |_file_02
        |_file_04
        file_03
        [COMP]:
        Path_A
        |_file_01
        Path_B
        |_file_02
        file_03
        """

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFilesInfo = [\
        {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_02', 'dir':2,'hash':'0000000000000000000000000000000F'},
        {'name':'file_03', 'dir':0,'hash':'000000000000000000000000000000FF'},
        {'name':'file_04', 'dir':2,'hash':'00000000000000000000000000000FFF'}]
        refLfPropertyMock = um.PropertyMock(return_value=refFilesInfo)
        type(refPsObj).libFiles = refLfPropertyMock
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFileInfo = [\
        {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_02', 'dir':2,'hash':'0000000000000000000000000000000F'},
        {'name':'file_03', 'dir':0,'hash':'000000000000000000000000000000FF'}]
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))
        hdict = {\
        '00000000000000000000000000000000':[compFileInfo[0],],
        '0000000000000000000000000000000F':[compFileInfo[1],],
        '000000000000000000000000000000FF':[compFileInfo[2],]}
        compPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=hdict))
        type(compPsObj).libFiles = um.PropertyMock(return_value=None) # unused --> the 'new files' detection

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        missing = sorted(handlerObj.missing, key=(lambda m: m.refName))

        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        getRelPathCalls = [um.call(0), um.call(1), um.call(2)]
        refPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)
        refLfPropertyMock.assert_called_with()

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        compPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)
        matchHashCalls = [um.call('00000000000000000000000000000000'), um.call('0000000000000000000000000000000F'), um.call('000000000000000000000000000000FF')]
        compPsObj.matchHash.assert_has_calls(matchHashCalls, any_order=True)
        self.assertEqual(compPsObj.matchHash.call_count,4)

        # Assertion on the properties of the 'compare.Misnaming' object
        self.assertEqual(len(missing),1)

        self.assertEqual(missing[0].refName, 'file_04')
        self.assertEqual(missing[0].refPath, 'Path_B')
        #MISSING: [REF]/Path_B/file_06
        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#MISSING: [REF]/Path_B/file_04 in [COMP]\n']
        self.assertEqual(missing[0].action(), actionMessage)

        # Testing output of method compare.Misnaming.shell()
        shellCommands = ['# Missing file $REF/Path_B/file_04 in $COMP\n',
        'cp $REF/Path_B/file_04 $COMP/Path_B/file_04\n']
        self.assertEqual(missing[0].shell(), shellCommands)

    def test_new(self):
        """
        [REF]:
        Path_A
        |_file_01
        Path_B
        |_file_02
        file_03
        [COMP]:
        Path_A
        |_file_01
        Path_B
        |_file_02
        |_file_04
        file_03
        """

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFilesInfo = [\
        {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_02', 'dir':2,'hash':'0000000000000000000000000000000F'},
        {'name':'file_03', 'dir':0,'hash':'000000000000000000000000000000FF'}]
        type(refPsObj).libFiles = um.PropertyMock(return_value=refFilesInfo)
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))
        refHdict = {\
        '00000000000000000000000000000000':[refFilesInfo[0],],
        '0000000000000000000000000000000F':[refFilesInfo[1],],
        '000000000000000000000000000000FF':[refFilesInfo[2],]}
        refPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=refHdict))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFileInfo = [\
        {'name':'file_01', 'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_02', 'dir':2,'hash':'0000000000000000000000000000000F'},
        {'name':'file_03', 'dir':0,'hash':'000000000000000000000000000000FF'},
        {'name':'file_04', 'dir':2,'hash':'00000000000000000000000000000FFF'}]
        type(compPsObj).libFiles = um.PropertyMock(return_value=compFileInfo)
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))
        compHdict = {\
        '00000000000000000000000000000000':[compFileInfo[0],],
        '0000000000000000000000000000000F':[compFileInfo[1],],
        '000000000000000000000000000000FF':[compFileInfo[2],],
        '00000000000000000000000000000FFF':[compFileInfo[3],]}
        compPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=compHdict))

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        news = sorted(handlerObj.new, key=(lambda m: m.compName))

        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Check calls to Mock object 'refPsObj' and PropertyMock object 'refLfPropertyMock'
        getRelPathCalls = [um.call(0), um.call(1), um.call(2)]
        refPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)

        # Check calls to Mock object 'compPsObj' and PropertyMock object 'compLfPropertyMock'
        matchHashCalls = [um.call('00000000000000000000000000000000'), um.call('0000000000000000000000000000000F'),
        um.call('000000000000000000000000000000FF'), um.call('00000000000000000000000000000FFF')]
        refPsObj.getRelPath.assert_has_calls(getRelPathCalls, any_order=True)

        # Assertion on the properties of the 'compare.News' object
        self.assertEqual(len(news),1)

        self.assertEqual(news[0].compName, 'file_04')
        self.assertEqual(news[0].compPath, 'Path_B')

        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#NEW: [COMP]/Path_B/file_04\n']
        self.assertEqual(news[0].action(), actionMessage)

        # Testing output of method compare.Misnaming.shell()
        shellCommands = ['# New file $COMP/Path_B/file_04\n',
        'cp $COMP/Path_B/file_04 $REF/Path_B/file_04\n']
        self.assertEqual(news[0].shell(), shellCommands)


    def test_redundancy(self):
        """
        [REF]:
        Path_A
        |_file_01
        |_file_01a (=file_01)
        Path_B
        |_file_01 (=file_01)
        |_file_02
        file_01b (=file_01)
        file_03
        [COMP]
        """

        # Mock object for the reference PathScan object
        refPsObj = um.Mock(spec_set=PathScan, name='mock_refPathScan')
        refFilesInfo = [\
        {'name':'file_01',  'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_01a', 'dir':1,'hash':'00000000000000000000000000000000'},
        {'name':'file_01',  'dir':2,'hash':'00000000000000000000000000000000'},
        {'name':'file_02',  'dir':2,'hash':'0000000000000000000000000000000F'},
        {'name':'file_01b', 'dir':0,'hash':'00000000000000000000000000000000'},
        {'name':'file_03',  'dir':0,'hash':'000000000000000000000000000000FF'}]
        type(refPsObj).libFiles = um.PropertyMock(return_value=refFilesInfo)
        refPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:'',1:'Path_A',2:'Path_B'}))
        refHdict = {\
        '00000000000000000000000000000000':[refFilesInfo[0],refFilesInfo[1],refFilesInfo[2],refFilesInfo[4]],
        '0000000000000000000000000000000F':[refFilesInfo[3],],
        '000000000000000000000000000000FF':[refFilesInfo[5],]}
        refPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=refHdict))

        # Mock object for the compared PathScan object
        compPsObj = um.Mock(spec_set=PathScan, name='mock_compPathScan')
        compFileInfo = []
        type(compPsObj).libFiles = um.PropertyMock(return_value=compFileInfo)
        compPsObj.getRelPath = um.Mock(side_effect=lambda dirId: self.getRelPath(dirId,{0:''}))
        compHdict = dict()
        compPsObj.matchHash = um.Mock(side_effect= lambda num: self.matchHash(hashNum=num, hashDict=compHdict))

        #------------------------ C R E A T I O N   &   O P E R A T I O N S ------------------------

        # Create object 'handlerObj' from class compare.Handler to be tested
        handlerObj = Handler(refPsObj, compPsObj)

        # Get the 'compare.Misnaming' object created by 'handlerObj'
        redundancies = sorted(handlerObj.redundancy, key=(lambda r: r.hashVal))

        #----------------------------------- A S S E R T I O N S -----------------------------------

        # Assertion on the properties of the 'compare.News' object
        self.assertEqual(len(redundancies),1)

        self.assertEqual(redundancies[0].hashVal, '00000000000000000000000000000000')
        files = [('Path_A','file_01'),('Path_A','file_01a'),('Path_B','file_01'),('','file_01b')]
        self.assertEqual(redundancies[0].files, files)

        # Testing output of method compare.Misnaming.action()
        actionMessage = ['#REDUNDANCY:\n',
        '  * [REF]/Path_A/file_01\n',
        '  * [REF]/Path_A/file_01a\n',
        '  * [REF]/Path_B/file_01\n',
        '  * [REF]/file_01b\n']
        self.assertEqual(redundancies[0].action(), actionMessage)

        # Testing output of method compare.Misnaming.shell()
        shellCommands = ['# Redundancy: manual operation must be considered\n',]
        self.assertEqual(redundancies[0].shell(), shellCommands)



if __name__=='__main__':

    unittest.main()
