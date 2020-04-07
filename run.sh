#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

cd /Users/ll3Ynxnj/Projects/BashProjects/aikiki/

# Clean data
rm -f ./DataSource/*

# Input data
cp /Users/ll3ynxnj/Public/ALGIO/* ./DataSource/

# Generate label data
/Users/ll3ynxnj/.pyenv/shims/python3 genDataFromCsv.py

# Print label
./printLabels.sh

# Output data
cp ./OrderLists/* /Users/ll3ynxnj/Public/ALGIO/

# Archive data
./addToArchive.sh
