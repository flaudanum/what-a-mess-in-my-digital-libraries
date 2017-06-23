# coding: UTF-8
"""
This module provides class PathScan
Compatibility: python 3.5 (required by os.DirEntry)
"""

import os
import hashlib
import json

class PathScan:
    """
    Abstraction for providing the data structure stemming from the scan of a path.

    :param path: path to the scanned directory
    :type path: str
    :param question: If a directory has already been scanned, is it asked to the user whether the directory should scanned again.
    :type question: bool
    :raises OSError: when the value of path is not an existing directory
    """

    saveFilename = '.whamdil.json'

    @property
    def path(self):
        """
        :returns: the path of the scanned directory
        :rtype: str
        """
        return self.__path

    @property
    def saveFilePath(self):
        """
        :returns: the path of the JSON save file with the scanning data
        :rtype: str
        """
        return os.path.join(self.path,PathScan.saveFilename)

    @property
    def directories(self):
        """
        :returns: information on sub-directories in the scanned directory [{'name': directory name, 'par': ID of the parent directory, 'id': ID of the directory}]
        :rtype: list( {'name':str, 'par':int, 'id':int} )
        """
        return self.__directories

    @property
    def libFiles(self):
        """
        :returns: information on every file in the path [{'name':file name, 'dir': ID of the directory where the file is, 'hash':MD5 hash number} ]
        :rtype: list( {'name':str, 'dir': int, 'hash': str} )
        """
        return self.__libFiles

    @staticmethod
    def md5sum(filePath):
        """
        Compute the md5 sum of a file

        :param filePath: path to the file
        :type filePath: str
        :returns: MD5 cryptographic hash number
        :rtype: str
        """
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(filePath, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

        return hasher.hexdigest()


    def __init__(self, path, question=True):

        # Check and store the path to scan
        if not(os.path.isdir(path)):
            raise OSError('class PathScan, contructor:\nNo such directory:\n'+path)
        self.__path = os.path.abspath(path)

        if os.path.isfile(self.saveFilePath):
            print('A scan result file is present in directory:\n{0}'.format(self.path))
            ans = None
            while not(ans in ('y','n','')):
                ans = input('Do you want to re-scan the path? (y/[n]):').lower()
            if ans in ('n',''):
                (self.__directories, self.__libFiles) = self.__json()
                return
            else:
                os.unlink(self.saveFilePath)

        self.__directories = []
        self.__libFiles = []

        self.__idCount = 0

        def scanPathTree(scanIter, dirName=None, parId=None):
            """
            Scan recursively the tree of directories in the path
            """

            # list with elements of the iterator scanIter, used for generating an multiple copies iterators
            scanSource = list(scanIter)

            # List of objects from class os.DirEntry associated to directories (no links) and sorted by name
            childDirs = sorted([ dEnt for dEnt in iter(scanSource) if dEnt.is_dir(follow_symlinks=False)], key=lambda dEnt: dEnt.name)

            # Files entries in the element (no symbolic links)
            files = sorted([ dEnt for dEnt in iter(scanSource) if dEnt.is_file(follow_symlinks=False)], key=lambda dEnt: dEnt.name)

            dirId = self.__idCount
            self.__idCount += 1
            if dirName:
                self.__directories.append({'name':dirName, 'par':parId, 'id':dirId})
            if files:
                self.__libFiles += [ {'name':dEnt.name, 'dir':dirId, 'hash':PathScan.md5sum(dEnt.path)} for dEnt in files]
            if childDirs:
                for dEnt in childDirs:
                    scanPathTree(scanIter=os.scandir(dEnt.path),dirName=dEnt.name, parId=dirId)

        scanPathTree(scanIter=os.scandir(self.path))


        # Save scanned information in a file inside the scanned path
        self.__save()

    def __json(self):
        """
        Read scan data from a JSON file.

        :returns (directories, libFiles):
        :rtype: list(list(dict()),list(dict()))
        """
        with open(self.saveFilePath,'rb') as buffRder:
            output = buffRder.read().decode('UTF-8')
        savedData = json.loads(output)

        directories = savedData['directories']
        libFiles = sorted(savedData['libFiles'], key=(lambda d: d['name']))
        return (directories, libFiles)


    def __save(self):
        """
        Save main data from the current PathScan instance in a JSON file.
        """
        jsonFormatted = json.dumps({'directories':self.directories,'libFiles':self.libFiles})
        with open(self.saveFilePath,'w') as txtIOWrper:
            txtIOWrper.write(jsonFormatted)

    def matchHash(self, hashNum):
        """
        Get files matching the MD5 hash number 'hashNum'.
        """
        return [info for info in self.libFiles if info['hash']==hashNum]

    def getRelPath(self,dirId):
        """
        Get the path (relative to the main scanned path) of the directory whith ID number 'dirId'.
        """
        def getDirDict(dirId):
            for d in self.directories:
                if d['id']==dirId:
                    return d
            return None

        if dirId==0: # Root directory
            return ''

        dirDict = getDirDict(dirId)
        if dirDict==None: # the directory entry does not exists
            return None
        if dirDict['par']==0:
            return dirDict['name']
        else:
            return os.path.join(self.getRelPath(dirDict['par']), dirDict['name'])
