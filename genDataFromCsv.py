# coding:utf-8

import csv
from enum import Enum
from labelGenerater import LabelGenerater

## 注文状況コード
class OrderItemStatus(Enum) :
    NOT_PAYMENT = 0
    WAITING_FOR_SHIPPING = 1
    SHIPPED = 2
    CANCELED = 3

    NONE = -1


## 注文ユーティリティ
class OrderUtility :
    ## 文字列から注文状況コードを取得
    @staticmethod
    def getStatus(aStatus) :
        orderItemStatus = OrderItemStatus.NONE
        return orderItemStatus


    ## 文字列から商品コードを取得
    @staticmethod
    def getProductCode(aProduct) :
        return 'test'


## 注文マネージャー
class OrderManager :
    def __init__(self) :
        self.orders = {} # IDをキーとする注文辞書（重複不可）


    ## 注文を初期化（CSVから取り込み）
    def initOrdersFromCsv(self, aOrders) :
        self.orders.clear()
        for order in aOrders :
            orderIdentifier = order['注文ID']
            isExist = orderIdentifier in self.orders.keys()
            if (isExist) :
                orderItem = self.orders[orderIdentifier]
            else :
                orderItem = OrderItem(orderIdentifier,
                                      OrderUtility.getStatus(order['注文状況']),
                                      order['配送先の住所1'],
                                      order['配送先の住所2'],
                                      order['配送先の氏名'])
                self.orders[orderIdentifier] = orderItem

            ## 商品名から商品コードを抽出して追加
            productCode = OrderUtility.getProductCode(order['作品名'])
            orderItem.addProduct(productCode)


    ## 注文を出力
    def printOrders(self) :
        for order in self.orders.values() :
            print ('--------')
            print (order.identifier)
            print (order.status)
            print (order.addressLine0)
            print (order.addressLine1)
            print (order.customerName)
            print (order.products)

    ## 注文を追加（IDが既に存在する場合はエラー終了）


    ## 注文を取得


## 注文項目
class OrderItem :
    def __init__(self, aIdentifier, aStatus,
                 aAddressLine0, aAddressLine1, aCustomerName) :
        self.identifier   = aIdentifier
        self.status       = aStatus
        self.addressLine0 = aAddressLine0
        self.addressLine1 = aAddressLine1
        self.customerName = aCustomerName
        self.products     = []


    ## 商品を追加
    def addProduct(self, aProduct) :
        self.products.append(aProduct)


with open('orders.csv', 'rb') as source :
    orderManager = OrderManager()
    orderManager.initOrdersFromCsv(csv.DictReader(source))
    orderManager.printOrders()
