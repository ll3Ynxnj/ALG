# coding:utf-8

import glob

from orderManager import OrderManager
from labelManager import LabelManager
from labelManager import LabelItem
from util import Util

dataSource = './DataSource/*.csv'
print(glob.glob(dataSource))
orderManager = OrderManager()
labelManager = LabelManager();
labelItems = list();
fileList = glob.glob(dataSource);
for filename in fileList :
    with open(filename, 'r', encoding='utf-8-sig') as filedata:
        csvDictFormat = Util.Csv.getCsvFormat(filedata)
        if csvDictFormat == Util.Order.Format.MINNE :
            orderManager.addOrderWithFileForMinne(filename)
        elif csvDictFormat == Util.Order.Format.CREEMA :
            orderManager.addOrderWithFileForCreema(filename)
        elif csvDictFormat == Util.Order.Format.PRINTING_LABELS :
            labelItems.append(labelManager.addItemWithFile(filename))
        else :
            print('filename : ' + filename)
            print('Unexpected CSV format detected.')
            sys.exit()

# 注意：現状、以下２つのprintに注文フォーマットが「PRINTING_LABELS」の分はprintされないので注意（今後どうするかは未定）
orderManager.printOrders()
orderManager.printOrdersByProduct()

for orderItem in orderManager.orders.values() :
    labelItems.append(labelManager.addItemWithOrder(orderItem))

labelManager.genLabel();
