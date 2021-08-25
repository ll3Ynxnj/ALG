#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

# Load configuration
. /usr/local/etc/alg.conf

# Setup directory
cd ${ALG_PATH}

# Clean data
rm -f ./DataSource/*

# Input data
cp ${ALG_PATH_TO_IO}/* ./DataSource/

# Convert to UTF-8
nkf --overwrite -w ./DataSource/*

# Generate CSV if convertible text exist
python3 genCsvFromText.py

# Generate label data
python3 genDataFromCsv.py

# Setup printer
lpoptions -p ${ALG_PRINTER_NAME} -o PageSize=29x90mm
lpoptions -p ${ALG_PRINTER_NAME} -o cupsPrintQuality=Normal

# Display print environment
# cat /etc/redhat-release
lpstat -s
lpoptions -p ${ALG_PRINTER_NAME} -l

# Print label
ls Labels/*.pdf | xargs lpr -o landscape -P ${ALG_PRINTER_NAME}

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

