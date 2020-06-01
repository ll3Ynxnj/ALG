# coding:utf-8

import sys
import glob
from util import Util

dataSource = './DataSource/*.txt'
print('-- Processing files ------------------------------------------------------------')
print(glob.glob(dataSource))
fileList = glob.glob(dataSource);
for filename in fileList :
    with open(filename, 'r', encoding='utf-8') as filedata:
        print('Processing : ' + filename)
        format = Util.Text.getFormat(filedata)
        if format == Util.Text.Format.ORDER_MINNE :
            Util.Text.genCsvWithFileForMinne(filedata)
        elif format == Util.Text.Format.ORDER_CREEMA :
            Util.Text.genCsvWithFileForCreema(filedata)
        elif format == Util.Text.Format.LABEL :
            Util.Text.genCsvWithFileForLabel(filedata)
        elif format == Util.Text.Format.LIST_PRODUCT :
            continue
        elif format == Util.Text.Format.LIST_CUSTOMER :
            continue
        else :
            print('ERROR : Unexpected Text format detected.')
            sys.exit()
