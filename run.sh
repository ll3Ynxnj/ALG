#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

cd /Users/ll3Ynxnj/Projects/BashProjects/aikiki/

# Clean data
rm -f ./DataSource/*

# Input data
cp /Users/ll3ynxnj/Public/ALGIO/* ./DataSource/

# Generate CSV if convertible text exist
/Users/ll3Ynxnj/.pyenv/shims/python3 genCsvFromText.py
#echo $?
#if ! `/Users/ll3Ynxnj/.pyenv/shims/python3 genCsvFromText.py`; then
#  echo "ERROR : genCsvFromText.py\n"
#  exit
#fi

# Generate label data
/Users/ll3Ynxnj/.pyenv/shims/python3 genDataFromCsv.py
#echo $?
#if ! `/Users/ll3Ynxnj/.pyenv/shims/python3 genDataFromCsv.py`; then
#  echo "ERROR : genDataFromCsv.py\n"
#  exit
#fi

# Print label
./printLabels.sh

# Output data
cp ./OrderLists/* /Users/ll3ynxnj/Public/ALGIO/

# Archive data
./addToArchive.sh
