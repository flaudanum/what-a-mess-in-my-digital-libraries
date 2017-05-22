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
