# coding:utf-8

import glob

from orderManager import OrderManager
from labelGenerater import LabelGenerater

orderManager = OrderManager()
dataSource = './DataSource/*.csv'
print(glob.glob(dataSource))
orderManager.initOrders(glob.glob(dataSource))
orderManager.printOrders()
orderManager.printOrdersByProduct()

labelGenerater = LabelGenerater();
for orderItem in orderManager.orders.values() :
    labelGenerater.genLabel(orderItem)
