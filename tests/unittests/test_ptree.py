# coding: UTF-8
"""
Unit tests for module 'ptree'
Compatibility: python 3.5
"""

import unittest
import os
import sys
sys.path += ('../../whamdil',)
import subprocess
import shutil
import json

from ptree import *

# Path_A
# |_Path_AA
# | |_file_01
# |_Path_AB
# | |_Path_ABA
# | | |_file_02
# | |_file_03
# |_file_04
# Path_B
# |_file_05
# |_file_06
# file_07
# file_08



class TestPathScan(unittest.TestCase):

    testCasesPath = os.path.abspath('../test_cases/')
    testedPath = './path01'

    @classmethod
    def setUpClass(cls):
        # Generation of the test case path 'path01' with script gen_path01.sh
        proc = subprocess.Popen(['bash',os.path.join(TestPathScan.testCasesPath, 'gen_path01.sh')])
        proc.communicate()

        # Creation of a PathScan object associated to pass 'path01'
        cls.pTreeObj = PathScan(TestPathScan.testedPath)

        # Reading MD5 hash numbers of files in 'path01' provided by the shell tool md5sum
        with open('md5_path01.txt','r') as ioObj:
            formatMD5res = lambda pair:( pair[1].split('/')[-1], pair[0])
            cls.refMD5 = dict([formatMD5res(line.split(None)) for line in ioObj])

        cls.refDirectories = [\
        {'id':1,'par':0,'name':'Path_A'},
        {'id':2,'par':1,'name':'Path_AA'},
        {'id':3,'par':1,'name':'Path_AB'},
        {'id':4,'par':3,'name':'Path_ABA'},
        {'id':5,'par':0,'name':'Path_B'}
        ]

        refFilesDir = dict((\
        ('file_01',2),
        ('file_02',4),
        ('file_03',3),
        ('file_04',1),
        ('file_05',5),
        ('file_06',5),
        ('file_07',0),
        ('file_08',0)
        ))
        cls.refLibFiles = [ {'name':k,'dir':refFilesDir[k],'hash':cls.refMD5[k]} for k in sorted(cls.refMD5.keys())]


    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(TestPathScan.testedPath):
            shutil.rmtree(TestPathScan.testedPath)
        os.unlink('md5_path01.txt')


    def test_path(self):
        ptObj = TestPathScan.pTreeObj
        self.assertEqual(ptObj.path, os.path.abspath(TestPathScan.testedPath))

    def test_directories(self):
        directories = TestPathScan.pTreeObj.directories

        for (ref,test) in zip(TestPathScan.refDirectories,directories):
            self.assertEqual(ref,test)

    def test_libFiles(self):
        libFiles = sorted(TestPathScan.pTreeObj.libFiles, key=(lambda d: d['name']))

        self.assertEqual(TestPathScan.refLibFiles,libFiles)

    def test_getRelPath(self):
        path = TestPathScan.pTreeObj.getRelPath(4)
        nopath = TestPathScan.pTreeObj.getRelPath(12)

        self.assertEqual(path,'Path_A/Path_AB/Path_ABA')
        self.assertIsNone(nopath)

    def test_matchHash(self):
        file01Hash = TestPathScan.refLibFiles[0]['hash']
        fileInfo = TestPathScan.pTreeObj.matchHash(file01Hash)
        self.assertEqual(fileInfo, TestPathScan.refLibFiles[0])


    def test_saveFile(self):
        with open(TestPathScan.testedPath+'/.whamdil.json','rb') as buffRder:
            output = buffRder.read().decode('UTF-8')
        savedData = json.loads(output)

        directories = savedData['directories']
        libFiles = sorted(savedData['libFiles'], key=(lambda d: d['name']))

        for (ref,test) in zip(TestPathScan.refDirectories,directories):
            self.assertEqual(ref,test)

        self.assertEqual(TestPathScan.refLibFiles,libFiles)




if __name__=='__main__':

    unittest.main()