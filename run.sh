#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

cd ~/Projects/BashProjects/aikiki/

# Clean data
rm -f ./DataSource/*

# Input data
cp ~/Public/ALGIO/* ./DataSource/

# Generate CSV if convertible text exist
~/.pyenv/shims/python3 genCsvFromText.py

# Generate label data
~/.pyenv/shims/python3 genDataFromCsv.py

# Print label
./printLabels.sh

# Output data
cp ./OrderLists/* ~/Public/ALGIO/

# Archive data
./addToArchive.sh
