
# Path_A
# |_Path_AA
# | |_file_01
# |_Path_AB
# | |_Path_ABA
# | | |_file_02
# | |_file_03
# |_file_04
# Path_B
# |_file_01
# |_file_05
# |_file_06
# file_07
# file_08


# Path to the main directory

MAIN_PATH='./path01'

if [ -d $MAIN_PATH ]; then
    rm -fr $MAIN_PATH
fi
mkdir $MAIN_PATH
cd $MAIN_PATH


# Creation of directries

mkdir Path_A
mkdir Path_A/Path_AA
mkdir Path_A/Path_AB
mkdir Path_A/Path_AB/Path_ABA
mkdir Path_B

# Creation of a file with a list of MD5 hash values of files

MD5LOGFILE=../md5_path01.txt
rm -f $MD5LOGFILE
touch $MD5LOGFILE


# Generation of files

# file_01
head -c 256000 /dev/urandom > Path_A/Path_AA/file_01
cp -p Path_A/Path_AA/file_01 Path_B/file_01 
md5sum Path_A/Path_AA/file_01 >> $MD5LOGFILE
# file_02
head -c 256000 /dev/urandom > Path_A/Path_AB/Path_ABA/file_02
md5sum Path_A/Path_AB/Path_ABA/file_02 >> $MD5LOGFILE
# file_03
head -c 256000 /dev/urandom > Path_A/Path_AB/file_03
md5sum Path_A/Path_AB/file_03 >> $MD5LOGFILE
# file_04
head -c 256000 /dev/urandom > Path_A/file_04
md5sum Path_A/file_04 >> $MD5LOGFILE

md5sum Path_B/file_01 >> $MD5LOGFILE

# file_05
head -c 256000 /dev/urandom > Path_B/file_05
md5sum Path_B/file_05 >> $MD5LOGFILE
# file_06
head -c 256000 /dev/urandom > Path_B/file_06
md5sum Path_B/file_06 >> $MD5LOGFILE
# file_07
head -c 256000 /dev/urandom > file_07
md5sum file_07 >> $MD5LOGFILE
# file_08
head -c 256000 /dev/urandom > file_08
md5sum file_08 >> $MD5LOGFILE
