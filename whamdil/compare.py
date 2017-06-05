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

        self.__refPathScan = refPathScan
        self.__compPathScan = compPathScan

        self.__misnaming = []

        for refInfo in self.refPathScan.libFiles:
            refFullPath = self.refPathScan.getRelPath(refInfo['dir'])
            for compInfo in self.compPathScan.matchHash(refInfo['hash']):
                compFullPath = self.compPathScan.getRelPath(compInfo['dir'])
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

    def __repr__(self):
        return 'Misnaming(path=\'{path}\',refName=\'{ref}\',compName=\'{comp}\')'.format(path=self.path,ref=self.refName,comp=self.compName)

    def action(self,form='text'):
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Misnaming, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        if self.path!='':
            message = ['#MISNAMING: [REF]/{0}/{1}\n'.format(self.path,self.refName),]
            message.append('Rename file [COMP]/{0}/{1}\n'.format(self.path,self.compName))
        else:
            message = ['#MISNAMING: [REF]/{0}\n'.format(self.refName),]
            message.append('Rename file [COMP]/{0}\n'.format(self.compName))

        return message

    def shell(self):
        if self.path!='':
            command = ['mv $COMP/{0}/{1} $COMP/{0}/{2}\n'.format(self.path,self.compName,self.refName),]
        else:
            command = ['mv $COMP/{0} $COMP/{1}\n'.format(self.compName,self.refName),]
        return command
