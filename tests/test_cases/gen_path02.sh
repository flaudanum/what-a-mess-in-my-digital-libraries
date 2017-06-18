# Content of path01:
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


# Content of path02:
# Path_A
# |_Path_AA
# | |_file_01
# | |_file_07C (file_07)
# |_Path_AB
# | |_Path_ABA
# | | |_file_02C (file_02)
# | | |_file_07 (file_07)
# | | |_file_08
# | |_file_03
# |_file_04
# |_file_09
# Path_B
# |_file_05
# file_02CC (file_02)
# file_08
# file_10


# Path to the main directory
REF_PATH='./path01'
MAIN_PATH='./path02'


if [ -d $MAIN_PATH ]; then
    rm -fr $MAIN_PATH
fi

bash gen_path01.sh

cp -rp $REF_PATH $MAIN_PATH

# MAIN PATH
rm $MAIN_PATH/file_07
cp $REF_PATH/Path_A/Path_AB/Path_ABA/file_02 $MAIN_PATH/file_02CC
head -c 128000 /dev/urandom > $MAIN_PATH/file_10

# Path_A
head -c 128000 /dev/urandom > $MAIN_PATH/Path_A/file_09

# Path_B
rm $MAIN_PATH/Path_B/file_06

# Path_AA
cp $REF_PATH/file_07 $MAIN_PATH/Path_A/Path_AA/file_07C
# _Path_ABA
mv $MAIN_PATH/Path_A/Path_AB/Path_ABA/file_02 $MAIN_PATH/Path_A/Path_AB/Path_ABA/file_02C
cp $REF_PATH/file_07 $MAIN_PATH/Path_A/Path_AB/Path_ABA/file_07
cp $REF_PATH/file_08 $MAIN_PATH/Path_A/Path_AB/Path_ABA/file_08
