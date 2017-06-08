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
|**Postcondition**        |* The tested path is compared with the reference path and the differences are identified:       |
|                         |                                                                                                |
|                         |  * The files missing in the tested path                                                        |
|                         |  * The additional files that are not in the reference path                                     |
|                         |  * The files which paths are the same but which names differs (misnaming)                      |
|                         |  * The files that are present in both paths but at different locations (misplacement)          |
|                         |  * The redundancy, that is the files that appear several times in the reference and tested     |
|                         |    paths                                                                                       |
|                         |                                                                                                |
|                         |* The differences are listed in text file with a description of associated corrective actions   |
|                         |* A shell script for performing the corrective actions is created                               |
+-------------------------+------------------------------------------------------------------------------------------------+
|**Technology**           |* The reference path and the tested one are specified as arguments of the run script in the     |
|                         |  shell                                                                                         |
+-------------------------+------------------------------------------------------------------------------------------------+
