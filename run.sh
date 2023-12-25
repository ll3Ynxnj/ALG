#!/bin/sh -xeu

export LC_CTYPE=ja_JP.UTF-8

# Load configuration
. /usr/local/etc/asc.conf

# Options
FLG_PRINT=FALSE
VAL_PRINTER_NAME=${ALG_PRINTER_NAME}
VAL_STATUS=all
OPT=
while getopts pS:P: OPT
do
  case $OPT in
		p) FLG_PRINT=TRUE
			;;
    S) VAL_STATUS=$OPTARG
			case $VAL_STATUS in
				all) echo "ORDER : All"
					;;
				w)  echo "ORDER : WaitingForShipping"
					;;
				s)   echo "ORDER : Shipped"
					;;
				*)   echo "ORDER : ERROR : $VAL_STATUS is undefined order."
					;;
			esac
			;;
    P) VAL_PRINTER_NAME=$OPTARG
			echo "PRINTER_NAME : $VAL_PRINTER_NAME"
      ;;
    \?) echo "Usage: $0 [-f] [-v value]" 1>&2
      exit 1
      ;;
  esac
done
shift `expr $OPTIND - 1`

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
python3 genDataFromCsv.py $VAL_STATUS
wait

# Setup printer
lpoptions -p ${VAL_PRINTER_NAME} -o PageSize=29x90mm
lpoptions -p ${VAL_PRINTER_NAME} -o cupsPrintQuality=Normal

# Display print environment
# cat /etc/redhat-release
lpstat -s
lpoptions -p ${VAL_PRINTER_NAME} -l

# Print label
if $FLG_PRINT ; then
  ls Labels/*.pdf | xargs lpr -o landscape -P ${ALG_PRINTER_NAME}
fi

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

