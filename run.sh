#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

# Setup directory
cd /usr/local/bin/alg

# Load configuration
. ./alg.conf

# Clean data
rm -f ./DataSource/*

# Input data
cp ${ALG_PATH_TO_IO}/* ./DataSource/

# Generate CSV if convertible text exist
python3 genCsvFromText.py

# Generate label data
python3 genDataFromCsv.py

# Setup printer
lpoptions -p Brother_QL-720NW -o PageSize=29x90mm
lpoptions -p Brother_QL-720NW -o cupsPrintQuality=Normal

# Display print environment
cat /etc/redhat-release
lpstat -s
lpoptions -p Brother_QL-720NW -l

# Print label
lpr -o landscape -P Brother_QL-720NW Labels/*.pdf

# Output data
cp ./OrderLists/* ${ALG_PATH_TO_IO}

# Archive data
mkdir ${ALG_PATH_TO_ARCHIVE_LOCAL}
cp -r Labels ${ALG_PATH_TO_ARCHIVE_LOCAL}
cp -r OrderLists ${ALG_PATH_TO_ARCHIVE_LOCAL}
cp -r DataSource ${ALG_PATH_TO_ARCHIVE_LOCAL}
cp -r ${ALG_PATH_TO_ARCHIVE_LOCAL} ${ALG_PATH_TO_ARCHIVE}
rm Labels/*
rm OrderLists/*
rm DataSource/*

