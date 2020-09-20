#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

cd /usr/local/bin/alg/

# Clean data
rm -f ./DataSource/*

# Input data
cp /home/samba/ALGIO/* ./DataSource/

# Generate CSV if convertible text exist
python3 genCsvFromText.py

# Generate label data
python3 genDataFromCsv.py

# Print label
./printLabels.sh

# Output data
cp ./OrderLists/* /home/samba/ALGIO/

# Archive data
./addToArchive.sh
