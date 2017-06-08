# What a mess in my digital libraries!

**(CURRENTLY IN DEVELOPMENT)**

## About
*What a mess in my digital libraries!* (whamdil) is an application that I'm developing for re-organizing the several copies of my digital book libraries.  
I have a big collection of digital books and several versions of it. The fact is that these versions are on hard drives and flash disks located in different places. I get new documents from different sources (e.g. office, home) that I copy to the available version of my numerical library. A simple solution would be to store my files in the cloud but the access to cloud storages is usually banned at office.  
At some point I need to get a unique version of my digital library that contains every file from every library classified in the same paths. I also do not want any duplication of my files (especially those with different names). That is where **whamdil** helps.

## Install
The application have been developped on Linux and only tested on it. A windows version may come later. No installation kit is available yet (to be done *asap*) so for the moment just clone the directory in the place of your choice and add the `whamdil/` subdirectory to your `PATH` environement variable (Linux). Give execution rights to script `whamdil.py`:  
`$> chmod a+x whamdil.py`  

Run this python script in a *shell* (*e.g.* Bourne shell). For getting help, type:
```
$> whamdil.py -h
usage: whamdil.py [-h] refPath [compPath]

Compare and help you reorganize the multiple versions of your digital
libraries

positional arguments:
  refPath     Path of reference
  compPath    Path to compare to the reference

optional arguments:
  -h, --help  show this help message and exit
```

## Running tests
This application is developped with *test driven approach*. Tests are available in the `tests/unittests/` directory. They use the Python `unittest` pacakge.
```
$> cd tests/unittests/
$> python test_ptree.py
$> python test_compare.py
```
