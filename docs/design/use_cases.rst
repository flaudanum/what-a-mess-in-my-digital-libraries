Specification of use cases
==========================

Scan a path and identify files
------------------------------

+-------------------------+------------------------------------------------------------------------------------------------+
|**Precondition**         |Specification of the path to scan                                                               |
+-------------------------+------------------------------------------------------------------------------------------------+
|**Postcondition**        |* The structure of the path is stored in memory                                                 |
|                         |* Every file in the path and sub-pathes is uniquely identified with a cryptographic hash value  |
|                         |* This information must be saved in a file in the scanned path                                  |
+-------------------------+------------------------------------------------------------------------------------------------+
|**Technology**           |* The format of the save file is *JSON*                                                         |
|                         |* The path to scan is specified as an argument of the run script in the shell                   |
+-------------------------+------------------------------------------------------------------------------------------------+


Compare files in a path w/ respect to another
---------------------------------------------

+-------------------------+------------------------------------------------------------------------------------------------+
|**Precondition**         |Specification of the reference path and the tested path                                         |
+-------------------------+------------------------------------------------------------------------------------------------+
|**Postcondition**        |* The files missing in the tested path are identified                                           |
|                         |* The additional files that are not in the reference file are identified                        |
|                         |* List the files that are present in both paths but in different locations and potentially with |
|                         |  different names                                                                               |
|                         |* print a summary in an unformatted text file                                                   |
+-------------------------+------------------------------------------------------------------------------------------------+
|**Technology**           |* The reference path and the tested one are specified as arguments of the run script in the     |
|                         |  shell                                                                                         |
+-------------------------+------------------------------------------------------------------------------------------------+
