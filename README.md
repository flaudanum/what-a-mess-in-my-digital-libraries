# What a mess in my digital libraries!


## About
*What a mess in my digital libraries!* (whamdil) is an application that I'm developing for re-organizing the several copies of my digital book libraries.  
I have a big collection of digital books and several versions of it. The fact is that these versions are on hard drives and flash disks located in different places. I get new documents from different sources (e.g. office, home) that I copy to the available version of my numerical library. A simple solution would be to store my files in the cloud but the access to cloud storages is usually banned at office.  
At some point I need to get a unique version of my digital library that contains every file from every library classified in the same paths. I also do not want any duplication of my files (especially those with different names). That is where **whamdil** helps.

## Install
The application is being developped on Linux and was only tested on it. A windows version may come later.  
In order to install *What a mess in my digital libraries!*, copy the content of the repository to your installation path. Change directory to this path and run *GNU make*:
```
$> make
```
An executable `./scripts/whamdil` whill be created and unit tests of the source will be run. The absolute path to directory `./scripts/` may be added to the `PATH` environement variable. Then run this script in the *shell*. For getting help, type:
```
$> whamdil -h
usage: whamdil [-h] refPath [compPath]

Compare and help you reorganize the multiple versions of your digital
libraries.

positional arguments:
  refPath     Path of reference
  compPath    Path to be compared to the reference

optional arguments:
  -h, --help  show this help message and exit
```

## Running tests
This application is being developped with *test driven approach*. Tests are available in the `tests/unittests/` directory. They use the Python `unittest` pacakge.
```
$> cd tests/unittests/
$> python test_ptree.py
$> python test_compare.py
```

## Code documentation

More documentation about the code is available [HERE](./docs/_build/html/index.html).
