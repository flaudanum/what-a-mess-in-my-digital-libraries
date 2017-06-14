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

    @property
    def misplacement(self):
        return self.__misplacement

    @property
    def missing(self):
        return self.__missing

    def __init__(self, refPathScan, compPathScan):
        """
        """

        self.__refPathScan = refPathScan
        self.__compPathScan = compPathScan

        self.__misnaming = []
        self.__misplacement = []
        self.__missing = []

        # MISNAMING
        # Same files, same path, different names
        # MISPLACEMENT
        # Same files, different paths

        for refInfo in self.refPathScan.libFiles:
            # Path of the reference file
            refFullPath = self.refPathScan.getRelPath(refInfo['dir'])
            # List of files with the same hash number than the reference file
            matchedFiles = self.compPathScan.matchHash(refInfo['hash'])

            # If no match then create a Missing object and go to next iteration
            if not(bool(matchedFiles)):
                self.__missing.append(Missing(refPath=refFullPath,refName=refInfo['name']))
                continue

            # Test path equality
            def diffPath(info):
                fullPath = self.compPathScan.getRelPath(info['dir'])
                return fullPath!=refFullPath
            # Information list on misplaced copies of the reference file
            misplacedFiles = filter(diffPath, matchedFiles)
            # Create Misplacement instances
            compFounds = [ (self.compPathScan.getRelPath(info['dir']), info['name']) for info in misplacedFiles]
            if compFounds:
                self.__misplacement.append(Misplacement(refPath=refFullPath,refName=refInfo['name'],compFounds=compFounds))

            # Create Misnaming instances
            for compInfo in matchedFiles:
                compFullPath = self.compPathScan.getRelPath(compInfo['dir'])
                # MISNAMING CASE
                if (compFullPath==refFullPath) and (compInfo['name']!=refInfo['name']):
                    self.__misnaming.append(Misnaming(path=compFullPath, refName=refInfo['name'], compName=compInfo['name']))


    def describe(self,filepath='./whamdil.log'):
        """
        """
        text = []
        text.append('[REF]: {0}\n'.format(self.refPathScan.path))
        text.append('[COMP]: {0}\n'.format(self.compPathScan.path))
        text.append('\n')
        for mispl in self.misplacement:
            text+=mispl.action()
            text.append('\n')

        with open(filepath,'w') as txtIOWrapper:
            for line in text:
                txtIOWrapper.write(line)






class Misnaming:
    """
    """
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
        """
        TODO: Add a commented title before the shell command: #MISNAMING: [REF]...
        """
        if self.path!='':
            command = ['mv $COMP/{0}/{1} $COMP/{0}/{2}\n'.format(self.path,self.compName,self.refName),]
        else:
            command = ['mv $COMP/{0} $COMP/{1}\n'.format(self.compName,self.refName),]
        return command



class Misplacement:
    """
    """

    @property
    def refPath(self):
        return self.__refPath

    @property
    def refName(self):
        return self.__refName

    @property
    def compFounds(self):
        return self.__compFounds

    def __init__(self,refPath,refName,compFounds):
        """
        """
        self.__refPath = refPath
        self.__refName = refName
        self.__compFounds = compFounds

    def __repr__(self):
        return 'Misplacement(refPath=\'{refPath}\',refName=\'{refName}\',compFounds={compFounds})'.\
        format(refPath=self.refPath,refName=self.refName,compFounds=str(self.compFounds))

    def action(self,form='text'):
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Misnaming, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#MISPLACEMENT: [REF]{0}/{1}\n'.format(fp(self.refPath),self.refName),]
        message.append('Move file [COMP]{0}/{1} to [COMP]{2}/{3}\n'.format(fp(self.compFounds[0][0]),self.compFounds[0][1],fp(self.refPath),self.refName))
        message+=['Remove file [COMP]{0}/{1}\n'.format(fp(found[0]),found[1]) for found in self.compFounds[1:]]
        return message

    def shell(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# Misplaced copies of [REF]{0}/{1}\n'.format(fp(self.refPath),self.refName),]
        command.append('mv $COMP{0}/{1} $COMP{2}/{3}\n'.format(fp(self.compFounds[0][0]),self.compFounds[0][1],fp(self.refPath),self.refName))
        command+=['rm -i $COMP{0}/{1}\n'.format(fp(found[0]),found[1]) for found in self.compFounds[1:]]
        return command


class Missing:
    """
    """

    @property
    def refPath(self):
        return self.__refPath

    @property
    def refName(self):
        return self.__refName

    def __init__(self,refPath,refName):
        """
        """
        self.__refPath = refPath
        self.__refName = refName

    def __repr__(self):
        return 'Missing(refPath=\'{refPath}\',refName=\'{refName}'.format(refPath=self.refPath,refName=self.refName)


    def action(self,form='text'):
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Misnaming, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#MISSING: [REF]{0}/{1} in [COMP]\n'.format(fp(self.refPath),self.refName),]
        return message

    def shell(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        # Missing file [REF]/Path_A/file_01 in [COMP]\n
        command = ['# Missing file $REF{0}/{1} in $COMP\n'.format(fp(self.refPath),self.refName),]
        command.append('cp $REF{0}/{1} $COMP{0}/{1}\n'.format(fp(self.refPath),self.refName))
        return command
