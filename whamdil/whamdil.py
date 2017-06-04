# coding: UTF-8
"""
Compatibility: python 3.X
"""

import argparse
import os
import sys

from ptree import *


def scanPath(refPath):
    """
    Use case: Scan a path and identify files
    """

    pTreeObj = PathScan(refPath)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Compare and help you reorganize the multiple versions of your digital libraries')
    parser.add_argument('refPath', help='Path of reference')
    parser.add_argument('compPath', help='Path to compare to the reference',nargs=='?',default=None)
    args = parser.parse_args()

    # Use case: Scan a path and identify files
    scanPath(args.refPath)
