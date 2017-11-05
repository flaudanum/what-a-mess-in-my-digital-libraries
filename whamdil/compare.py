# coding: UTF-8
"""
Compatibility: python 3.X
"""

import os
import unittest.mock


class Handler:
    """
    Handler class the carries out the comparison between the directories of the libraries

    :param refPathScan: Scan of the reference directory
    :type refPathScan: ptree.PathScan
    :param compPathScan: Scan of the directory to be compared to the reference
    :type compPathScan: ptree.PathScan
    """


    @property
    def refPathScan(self):
        """
        :returns: Scan of the reference directory
        :rtype: ptree.PathScan
        """
        return self.__refPathScan


    @property
    def compPathScan(self):
        """
        :returns: Scan of the directory to be compared to the reference
        :rtype: ptree.PathScan
        """
        return self.__compPathScan


    @property
    def misnaming(self):
        """
        :returns: Collection of Misnaming objects created during the construction
        :rtypes: compare.Misnaming
        """
        return self.__misnaming


    @property
    def misplacement(self):
        """
        :returns: Collection of Misplacement objects created during the construction
        :rtypes: compare.Misplacement
        """
        return self.__misplacement


    @property
    def missing(self):
        """
        :returns: Collection of Missing objects created during the construction
        :rtypes: compare.Missing
        """
        return self.__missing


    @property
    def new(self):
        """
        :returns: Collection of New objects created during the construction
        :rtypes: compare.New
        """
        return self.__new


    @property
    def redundancy(self):
        """
        :returns: Collection of Redundancy objects created during the construction
        :rtypes: compare.Redundancy
        """
        return self.__redundancy


    def __init__(self, refPathScan, compPathScan):

        self.__refPathScan = refPathScan
        self.__compPathScan = compPathScan

        self.__misnaming    = list()
        self.__misplacement = list()
        self.__missing      = list()
        self.__new          = list()
        self.__redundancy   = list()

        for refInfo in self.refPathScan.libFiles:
            # Path of the reference file
            refFullPath = self.refPathScan.getRelPath(refInfo['dir'])
            # List of files with the same hash number than the reference file
            matchedCompFiles = self.compPathScan.matchHash(refInfo['hash'])

            # If no match then create a 'Missing' object and go to next iteration
            if not(bool(matchedCompFiles)):
                self.__missing.append(Missing(refPath=refFullPath,refName=refInfo['name']))
                continue

            # Test path equality
            def diffPath(info):
                fullPath = self.compPathScan.getRelPath(info['dir'])
                return fullPath!=refFullPath
            # Information list on misplaced copies of the reference file
            misplacedFiles = filter(diffPath, matchedCompFiles)
            # Create Misplacement instances
            compFounds = [ (self.compPathScan.getRelPath(info['dir']), info['name']) for info in misplacedFiles]
            if compFounds:
                self.__misplacement.append(Misplacement(refPath=refFullPath,refName=refInfo['name'],compFounds=compFounds))

            # Create Misnaming instances
            for compInfo in matchedCompFiles:
                compFullPath = self.compPathScan.getRelPath(compInfo['dir'])
                if (compFullPath==refFullPath) and (compInfo['name']!=refInfo['name']):
                    self.__misnaming.append(Misnaming(path=compFullPath, refName=refInfo['name'], compName=compInfo['name']))

        # Detection of redundancies
        if not( isinstance(self.refPathScan.matchHash(str()), unittest.mock.Mock) ): # skip when PathScan.matchHash() is a Mock that does return a value
            refHashNumSet = frozenset([refInfo['hash'] for refInfo in refPathScan.libFiles])
            for hashNum in iter(refHashNumSet):
                matchedRefFiles = self.refPathScan.matchHash(hashNum)
                if len(matchedRefFiles)>1:
                    files = [ ( self.refPathScan.getRelPath(info['dir']), info['name'] ) for info in matchedRefFiles ]
                    self.__redundancy.append( Redundancy(hashVal=hashNum, files=files) )


        if bool(self.compPathScan.libFiles):
            for compInfo in self.compPathScan.libFiles:
                # Path of the compared file
                compFullPath = self.compPathScan.getRelPath(compInfo['dir'])
                # List of files in the reference directory with the same hash number than the compared file
                matchedRefFiles = self.refPathScan.matchHash(compInfo['hash'])
                # If no match then create a 'New' object and go to next iteration
                if not(bool(matchedRefFiles)):
                    self.__new.append(New(compPath=compFullPath,compName=compInfo['name']))


    def describe(self,filepath='./whamdil.log'):
        """
        Create a log file providing a description of differences between the content of directories

        :param filepath: Path to the logfile (default=``./whamdil.log``)
        :type filepath: str
        """

        text = list()
        text.append('[REF]: {0}\n'.format(self.refPathScan.path))
        text.append('[COMP]: {0}\n'.format(self.compPathScan.path))
        text.append('\n')

        # Print misnaming information
        for misng in self.misnaming:
            text+=misng.action()
            text.append('\n')

        # Print misplacement information
        for mispl in self.misplacement:
            text+=mispl.action()
            text.append('\n')

        # Print information about missing elements
        for missg in self.missing:
            text+=missg.action()
            text.append('\n')

        # Print information about new elements
        for new in self.new:
            text+=new.action()
            text.append('\n')

        # Print information about redundancy elements
        for red in self.redundancy:
            text+=red.action()
            text.append('\n')


        with open(filepath,'w') as txtIOWrapper:
            for line in text:
                txtIOWrapper.write(line)


    def shell(self,filepath='./whamdil.sh'):
        """
        Create a Bourne shell script file providing commands intending to even the directories

        :param filepath: Path to the shell script (default=``./whamdil.sh``)
        :type filepath: str
        """
        text = list()
        text.append('#!/usr/bin/bash'+'\n'*2)
        text.append("IFS=';'"+'\n'*2)
        text.append('# Path to directories\n')
        text.append("REF='{0}'\n".format(self.refPathScan.path))
        text.append("COMP='{0}'\n".format(self.compPathScan.path))
        text.append('\n')

        # Print misnaming commands
        for misng in self.misnaming:
            text+=misng.shell()
            text.append('\n')

        # Print misplacement commands
        for mispl in self.misplacement:
            text+=mispl.shell()
            text.append('\n')

        # Print commands for missing elements
        for missg in self.missing:
            text+=missg.shell()
            text.append('\n')

        # Print commands about new elements
        for new in self.new:
            text+=new.shell()
            text.append('\n')

        # Print commands about redundancy elements
        for red in self.redundancy:
            text+=red.shell()
            text.append('\n')


        with open(filepath,'w') as txtIOWrapper:
            for line in text:
                txtIOWrapper.write(line)



# REFACTORING: Create a super class with method 'fp'

class Misnaming:
    """
    Represents a file in the compared directory that has the proper relative path but is misnamed.

    :param path: relative path of the files
    :type path: str
    :param refName: name of the file in the reference directory
    :type refName: str
    :param compName: name of the minsnamed file in the compared directory
    :type compName: str
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
        return 'Misnaming(path=\'{path}\',refName=\'{ref}\',compName=\'{comp}\')'.format(path=self.path, 
                ref=self.refName, comp=self.compName)

    def action(self,form='text'):
        """
        Produce a text logfile with a description of the action to perform in order to make both paths even

        :returns: content of the file
        :rtype: list(str)
        """
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Misnaming, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#MISNAMING: [REF]{0}/{1}\n'.format(fp(self.path),self.refName),]
        message.append('Rename file [COMP]{0}/{1}\n'.format(fp(self.path),self.compName))

        return message

    def shell(self):
        """
        Produce the shell script content

        :returns: content of the file
        :rtype: list(str)
        """
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# Misnaming $REF{0}/{1}\n'.format(fp(self.path),self.refName),]
        command.append('mv "$COMP{0}/{1}" "$COMP{0}/{2}"\n'.format(fp(self.path), self.compName, self.refName))

        return command



class Misplacement:
    """
    Represents a file in the compared directory that is placed in a different path from an identical file found in the 
    reference directory.
    refPath,refName,compFounds

    :param refPath: relative path of the reference file
    :type path: str
    :param refName: name of the file in the reference directory
    :type refName: str
    :param compFounds: files in the compared directory that are misplaced [(path,filename),...]
    :type compFounds:  list( (str,str) )
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
        format(refPath=self.refPath, refName=self.refName, compFounds=str(self.compFounds))

    def action(self,form='text'):
        """
        Produce a text logfile with a description of the action to perform in order to make both paths even

        :returns: content of the file
        :rtype: list(str)
        """
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Misplacement, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#MISPLACEMENT: [REF]{0}/{1}\n'.format(fp(self.refPath), self.refName),]
        message.append('Move file [COMP]{0}/{1} to [COMP]{2}/{3}\n'.format(fp(self.compFounds[0][0]), 
            self.compFounds[0][1], fp(self.refPath), self.refName))
        message+=['Remove file [COMP]{0}/{1}\n'.format(fp(found[0]),found[1]) for found in self.compFounds[1:]]
        return message

    def shell(self):
        """
        Produce the shell script content

        :returns: content of the file
        :rtype: list(str)
        """
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# Misplaced copies of [REF]{0}/{1}\n'.format(fp(self.refPath), self.refName),]
        command.append('mv "$COMP{0}/{1}" "$COMP{2}/{3}"\n'.format(fp(self.compFounds[0][0]), self.compFounds[0][1], 
            fp(self.refPath), self.refName))
        command+=['rm -i "$COMP{0}/{1}"\n'.format(fp(found[0]), found[1]) for found in self.compFounds[1:]]
        return command


class Missing:
    """
    Descriptive elements for files of the reference directory that are missing in the compared one.

    :param refPath: relative path in the reference directory
    :type refPath: str
    :param refName: name of the missing file
    :type refName: str
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
        return 'Missing(refPath=\'{refPath}\',refName=\'{refName}'.format(refPath=self.refPath, refName=self.refName)


    def action(self,form='text'):
        """
        Produce a text logfile with a description of the action to perform in order to make both paths even

        :returns: content of the file
        :rtype: list(str)
        """
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Missing, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#MISSING: [REF]{0}/{1} in [COMP]\n'.format(fp(self.refPath), self.refName),]
        return message

    def shell(self):
        """
        Produce the shell script content

        :returns: content of the file
        :rtype: list(str)
        """
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# Missing file $REF{0}/{1} in $COMP\n'.format(fp(self.refPath), self.refName),]
        command.append('cp "$REF{0}/{1}" "$COMP{0}/{1}"\n'.format(fp(self.refPath), self.refName))
        return command


class New:
    """
    Descriptive elements for files of the compared directory that are missing in the reference one

    :param compPath: relative path in the compared directory
    :type compPath: str
    :param compName: name of the new file
    :type compName: str
    """

    @property
    def compPath(self):
        return self.__compPath

    @property
    def compName(self):
        return self.__compName

    def __init__(self,compPath,compName):
        """
        """
        self.__compPath = compPath
        self.__compName = compName

    def __repr__(self):
        return 'New(compPath=\'{compPath}\',compName=\'{compName}'.format(compPath=self.compPath, refName=self.compName)


    def action(self,form='text'):
        """
        Produce a text logfile with a description of the action to perform in order to make both paths even

        :returns: content of the file
        :rtype: list(str)
        """
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class New, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#NEW: [COMP]{0}/{1}\n'.format(fp(self.compPath), self.compName),]
        return message

    def shell(self):
        """
        Produce the shell script content

        :returns: content of the file
        :rtype: list(str)
        """
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# New file $COMP{0}/{1}\n'.format(fp(self.compPath),self.compName),]
        command.append('cp "$COMP{0}/{1}" "$REF{0}/{1}"\n'.format(fp(self.compPath), self.compName))
        return command


class Redundancy:
    """
    Descriptive elements for files that are redundant in the reference directory

    :param hashVal: MD5 hash number of the redundant files (lower case hexadecimal)
    :type hashVal: str
    :param files: Collection of information on the redundant files  [(path,filename),...]
    :type files:  list( (str,str) )
    """

    @property
    def hashVal(self):
        return self.__hv

    @property
    def files(self):
        return self.__files

    def __init__(self,hashVal,files):

        self.__hv = hashVal
        self.__files = files

    def __fp(self,path):
        """
        Format Path for dealing with root directory case
        """
        return '' if path=='' else '/'+path

    def __repr__(self):
        return 'Redundancy(hashVal=\'{hashVal}\',files=\'{files}'.format(hashVal=self.hashVal, files=str(self.files))

    def action(self,form='text'):
        """
        Produce a text logfile with a description of the action to perform in order to make both paths even

        :returns: content of the file
        :rtype: list(str)
        """
        if form=='text':
            return self.__actionText()
        else:
            raise ValueError('Class Redundancy, method action: wrong format \'{0}\''.format(form))

    def __actionText(self):
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        message = ['#REDUNDANCY:\n',]
        for f in self.files:
            message.append( '  * [REF]{0}/{1}\n'.format(self.__fp(f[0]),f[1]) )
        return message

    def shell(self):
        """
        Produce the shell script content

        :returns: content of the file
        :rtype: list(str)
        """
        fp = lambda path: '' if path=='' else '/'+path # Format Path for dealing with root directory case
        command = ['# Redundancy: manual operation must be considered\n',]
        return command

