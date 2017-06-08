Description of test cases
=========================

Test case - path_01
-------------------

Here is the file structure of the path ``path_01``. This path is generated with the script
``/tests/test_cases/gen_path01.sh``.

::

    | Path_A
    | |_Path_AA
    | | |_file_01
    | |_Path_AB
    | | |_Path_ABA
    | | | |_file_02
    | | |_file_03
    | |_file_04
    | Path_B
    | |_file_05
    | |_file_06
    | file_07
    | file_08


The files ``file_**`` are unformatted files which content is created with the
random generator provided by the following shell command:

.. code-block:: bash

    head -c 256000 /dev/urandom > Path_to_the_file_with_random content

This test case is used by the unit tests script ``tests/unittests/test_ptree.py``.
