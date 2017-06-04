# coding: UTF-8
"""
Compatibility: python 3.X
"""

import os

class Handler:


    @property
    def refPathScan(self):
        return self.__refPathScan

    @property
    def compPathScan(self):
        return self.__compPathScan

    @property
    def misnaming(self):
        return self.__misnaming


    def __init__(self, refPathScan, compPathScan):
        """
        """

        # # Check and store the path to scan
        # if not(os.path.isdir(refPathScan)):
        #     raise OSError('class compare.Handler, contructor:\n\'refPathScan\' is not an existing directory:\n'+refPathScan)
        # if not(os.path.isdir(compPathScan)):
        #     raise OSError('class compare.Handler, contructor:\n\'compPathScan\' is not an existing directory:\n'+refPathScan)
        self.__refPathScan = refPathScan
        self.__compPathScan = compPathScan

        self.__misnaming = []

        for refInfo in self.refPathScan.libFiles:
            for compInfo in self.compPathScan.libFiles:
                if compInfo['hash']==refInfo['hash']:
                    compFullPath = self.compPathScan.getRelPath(compInfo['dir'])
                    refFullPath = self.refPathScan.getRelPath(compInfo['dir'])
                    if (compFullPath==refFullPath) and (compInfo['name']!=refInfo['name']):
                        self.__misnaming.append(Misnaming(path=compFullPath, refName=refInfo['name'], compName=compInfo['name']))




class Misnaming:

    @property
    def path(self):
        return self.__fullPath

    @property
    def refName(self):
        return self.__refName

    @property
    def compName(self):
        return self.__compName

    def __init__(self,path,refName,compName):
        self.__fullPath = path
        self.__refName  = refName
        self.__compName = compName

    def action(self):
        message = ['#MISNAMING: [REF]/{0}/{1}\n'.format(self.path,self.refName),]
        message.append('Rename file [COMP]/{0}/{1}\n'.format(self.path,self.compName))
        return message
