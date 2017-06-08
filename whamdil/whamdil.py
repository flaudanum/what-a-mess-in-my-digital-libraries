#!/usr/bin/env python
# coding: UTF-8
"""
Compatibility: python 3.X
"""

import argparse
import os
import sys

from ptree import *
from compare import *


def scanPath(refPath):
    """
    Use case: Scan a path and identify files
    """
    pScanObj = PathScan(refPath)


def comparePaths(refPath,compPath):
    """
    Use case: Compare files in a path w/ respect to another
    """
    refPathScanObj = PathScan(refPath)
    compPathScanObj = PathScan(compPath)
    handlerObj = Handler(refPathScanObj,compPathScanObj)
    handlerObj.describe()



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Compare and help you reorganize the multiple versions of your digital libraries')
    parser.add_argument('refPath', help='Path of reference')
    parser.add_argument('compPath', help='Path to compare to the reference',nargs='?',default=None)
    args = parser.parse_args()


    if args.compPath==None: # Only the required positional argument 'refPath' is provided
        # Use case: Scan a path and identify files
        scanPath(args.refPath)
    else: # The second optional positional argument 'compPath' is provided
        # Use case: Compare two paths
        comparePaths(args.refPath,args.compPath)
