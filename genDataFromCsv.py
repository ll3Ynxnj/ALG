# coding:utf-8

import sys
import glob

from orderManager import OrderManager
from labelManager import LabelManager
from labelManager import LabelItem
from util import Util

aStatus = sys.argv[1]
itemStatus = Util.Order.ItemStatus.NONE

print (sys.argv)
print ("STATUS: " + aStatus)
if aStatus == 'w':
    itemStatus = Util.Order.ItemStatus.WAITING_FOR_SHIPPING
elif aStatus == 's':
    itemStatus = Util.Order.ItemStatus.SHIPPED

dataSource = './DataSource/*.csv'
print(glob.glob(dataSource))
orderManager = OrderManager()
labelManager = LabelManager()
labelItems = list();
fileList = glob.glob(dataSource)
for filename in fileList :
    with open(filename, 'r', encoding='utf-8-sig') as filedata:
        print('Processing : ' + filename)
        csvDictFormat = Util.Csv.getCsvFormat(filedata)
        if csvDictFormat == Util.Order.Format.MINNE :
            orderManager.addOrderWithFileForMinne(filename, itemStatus)
        elif csvDictFormat == Util.Order.Format.CREEMA :
            orderManager.addOrderWithFileForCreema(filename, itemStatus)
        elif csvDictFormat == Util.Order.Format.BASE :
            orderManager.addOrderWithFileForBase(filename, itemStatus)
        elif csvDictFormat == Util.Order.Format.MANUAL_INPUT :
            orderManager.addOrderWithFileForManualInput(filename)
        elif csvDictFormat == Util.Order.Format.PRINTING_LABELS :
            labelManager.addItemWithFile(filename)
        else :
            print('Unexpected CSV format detected.')
            sys.exit(1)

orderManager.printOrders()
orderManager.printOrdersByProduct()

for orderItem in orderManager.orders.values() :
    labelManager.addItemWithOrder(orderItem)

labelManager.genLabel()

