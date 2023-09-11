# coding:utf-8

import os
import re
import sys
import csv
import pprint
import collections
from datetime import datetime
from enum import Enum
from util import Util

## 注文マネージャー
class OrderManager :
    def __init__(self) :
        self.orders = collections.OrderedDict() # IDをキーとする注文辞書（重複不可）


    ## 注文を追加（Minne）
    def addOrderWithFileForMinne(self, aFilename, aItemStatus) :
        print('CALLED : addOrderWithFileForMinne()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)

            dbg_row = 0
            for row in csvDict :
                #print (row)
                if 0 :
                    colOrderStatus = row['注文状況']
                    print ("STATUS : " + colOrderStatus)
                    if   aItemStatus == Util.Order.ItemStatus.WAITING_FOR_SHIPPING :
                        if colOrderStatus != '発送準備中' :
                            print ('minne 除外 (' + colOrderStatus + ')')
                            continue
                    elif aItemStatus == Util.Order.ItemStatus.SHIPPED :
                        if colOrderStatus != '発送完了' :
                            print ('minne 除外 (' + colOrderStatus + ')')
                            continue

                orderIdentifier = row['注文ID']

                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    orderItem = OrderItem(orderIdentifier,
                                          Util.Order.getStatus(row['注文状況']),
                                          '〒' + row['配送先の郵便番号'],
                                          row['配送先の住所1'] + ' ' +
                                          row['配送先の住所2'],
                                          row['配送先の氏名'])
                    self.orders[orderIdentifier] = orderItem

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = Util.Order.getProductCode(row['作品名'])

                for i in range(int(row['数量'])) :
                    orderItem.addProduct(productCode)

                # print(orderItem.products)
                ++dbg_row


    ## 注文を追加（Creema）
    def addOrderWithFileForCreema(self, aFilename, aItemStatus) :
        print('CALLED : addOrderWithFileForCreema()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)

            dbg_row = 0
            for row in csvDict :
                #print (row)
                # 注文状況による除外
                if 0 :
                    colOrderStatus = row['ステータス']
                    print ("STATUS : " + colOrderStatus)
                    if   aItemStatus == Util.Order.ItemStatus.WAITING_FOR_SHIPPING :
                        if colOrderStatus != '発送準備' :
                            print ('Creema 除外 (' + colOrderStatus + ')')
                            continue
                    elif aItemStatus == Util.Order.ItemStatus.SHIPPED :
                        if colOrderStatus != '発送完了' :
                            print ('Creema 除外 (' + colOrderStatus + ')')
                            continue

                if 0 :
                    orderIdentifier = row['注文ID']
                    ## 注文を追加（既に存在する注文は纏める）
                else :
                    orderIdentifier = '0'
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    strStatus = ''
                    if 0 :
                        strStatus = row['ステータス']
                    strPostalCode = ''
                    if 0 :
                        strPostalCode = row['郵便番号']
                    strAddress = ''
                    if 0 :
                        strAddress = row['住所']
                    strName = ''
                    if 0 :
                        strName = row['名前']


                    ## １件目の注文の場合はOrderItemを作成
                    postalCode = re.sub('[^0-9\-]', '', strPostalCode)
                    orderItem = OrderItem(orderIdentifier,
                                          Util.Order.getStatus(strStatus),
                                          '〒' + postalCode,
                                          strAddress,
                                          strName)
                    self.orders[orderIdentifier] = orderItem

                productString = row['作品タイトル'] + row['オプション1'] + row['オプション2']
                ## Creemaのギフトラッピングはコードを振れないので「あり」の文字列を探して存在すれば追加
                if 0 :
                    if 'あり' in row['ギフトラッピング'] :
                        productString += '-[W]'

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = Util.Order.getProductCode(productString)

                for i in range(int(row['数量'])) :
                    orderItem.addProduct(productCode)

                ++dbg_row


    ## 注文を追加（BASE）
    def addOrderWithFileForBase(self, aFilename, aItemStatus) :
        print('CALLED : addOrderWithFileForBase()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)
            dbg_row = 0
            for row in csvDict :
                # print(row)
                colOrderStatus = row['発送状況']
                print ("STATUS : " + colOrderStatus)
                if   aItemStatus == Util.Order.ItemStatus.WAITING_FOR_SHIPPING :
                    if colOrderStatus != '未発送' :
                        print ('BASE 除外 (' + colOrderStatus + ')')
                        continue
                elif aItemStatus == Util.Order.ItemStatus.SHIPPED :
                    if colOrderStatus != '発送済み' :
                        print ('BASE 除外 (' + colOrderStatus + ')')
                        continue

                orderIdentifier = row['注文ID']
                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    postalCode = re.sub('[^0-9\-]', '', row['郵便番号(配送先)'])
                    orderItem = OrderItem(orderIdentifier,
                                          Util.Order.getStatus(row['発送状況']),
                                          '〒' + postalCode,
                                          row['都道府県(配送先)'] + row['住所(配送先)'] + row['住所2(配送先)'],
row['氏(配送先)'] + ' ' + row['名(配送先)'])
                    self.orders[orderIdentifier] = orderItem

                productString = row['商品名'] + row['バリエーション']
                ## BASEのギフトラッピングはコードを振れないので「あり」の文字列を探して存在すれば追加
                if 'あり' in row['バリエーション'] and '商品オプション「ギフトラッピング」' in row['商品名']:
                    productString += '[00]-[W]'

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = Util.Order.getProductCode(productString)

                for i in range(int(row['数量'])) :
                    orderItem.addProduct(productCode)

                ++dbg_row


    ## 注文を追加（Shopify）
    def addOrderWithFileForShopify(self, aFilename, aItemStatus) :
        print('CALLED : addOrderWithFileForShopify()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)
            dbg_row = 0
            for row in csvDict :
                # print(row)
                colOrderStatus = row['Fulfillment Status']
                print ("STATUS : " + colOrderStatus)
                if   aItemStatus == Util.Order.ItemStatus.WAITING_FOR_SHIPPING :
                    if colOrderStatus != 'unfulfilled' : # 未発送
                        print ('Shopify 除外 (' + colOrderStatus + ')')
                        continue
                elif aItemStatus == Util.Order.ItemStatus.SHIPPED :
                    if colOrderStatus != 'fulfilled'   : # 発送済
                        print ('Shopify 除外 (' + colOrderStatus + ')')
                        continue

                orderIdentifier = row['Name']
                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    postalCode = re.sub('[^0-9\-]', '', row['Shipping Zip'])
                    orderItem = OrderItem(orderIdentifier,
                                          Util.Order.getStatus(row['Fulfillment Status']),
                                          '〒' + postalCode,
                                          row['Shipping Province Name'] + row['Shipping City'] + row['Shipping Street'],
                                          row['Shipping Company'] + ' ' + row['Shipping Name'])
                    self.orders[orderIdentifier] = orderItem
                productString = row['Lineitem name']
                matches = re.findall('\[[a-zA-Z0-9\-:]*\]', productString)

                if not matches:
                    raise ValueError("文字列「" + productString + "」から商品コードをみつけられませんでした")

                ## Shopifyでは選択肢にオプションコードを含まない運用にしたためここで特定文字列をオプションコードに変更する
                productString = Util.Order.convertProductString(productString)
                print("productString: ", productString)

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = Util.Order.getProductCode(productString)

                for i in range(int(row['Lineitem quantity'])) :
                    orderItem.addProduct(productCode)

                ++dbg_row


    ## 注文を追加（Manual Input)
    def addOrderWithFileForManualInput(self, aFilename) :
        print('CALLED : addOrderWithFileForManualInput()')
        with open(aFilename, 'r', encoding='utf-8') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)

            dbg_row = 0
            for row in csvDict :
                orderIdentifier = row['注文ID']

                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    orderItem = OrderItem(orderIdentifier,
                                          Util.Order.getStatus(''),
                                          row['住所0'],
                                          row['住所1'],
                                          row['氏名'])
                    self.orders[orderIdentifier] = orderItem
                    print('orderItem.customerName : {}'.format(orderItem.customerName))

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = Util.Order.getProductCode(row['商品'])

                orderItem.addProduct(productCode)

                ++dbg_row


    ## 注文を出力
    def printOrders(self) :
        print('CALLED : printOrders()')
        orderList = '-LIST-CUSTOMER\n\n'
        for order in self.orders.values() :
            orderList += str(order.identifier)
            orderList += '\n'
            orderList += str(order.addressLine0)
            orderList += ' '
            orderList += str(order.addressLine1)
            orderList += '\n'
            orderList += str(order.customerName)
            orderList += '\n'
            orderList += str(order.products)
            orderList += '\n\n'

        print (orderList)

        dateTimeNow = datetime.now()
        fileName = dateTimeNow.strftime('%y%m%d%h%m%s')
        filePath = 'OrderLists/order_' + fileName + '.txt'
        with open(filePath, 'w') as f :
            f.write(orderList)
            os.chmod(filePath, 0o777)


    ## 注文を製品毎に取得
    def getOrdersByProduct(self) :
        print("CALLED : getOrdersByproduct()")
        orders = {}
        for order in self.orders.values() :
            for product in order.products :
                if (not product in orders) :
                    orders[product] = 0
                orders[product] += 1
        return orders


    ## 注文を製品毎に出力
    def printOrdersByProduct(self) :
        print("CALLED : printOrdersByProduct()")
        orders = self.getOrdersByProduct()

        ## 製品名で並び替え
        sortedOrders = sorted(orders.items());

        ## 製品名ごとに辞書を作成して出力
        categories = {};
        for order in sortedOrders :
            categoryCode = Util.Order.getCategoryCode(order[0])
            if (categoryCode not in categories) :
                categories[categoryCode] = []
            categories[categoryCode].append(order)

        sortedCategories = collections.OrderedDict()

        ## 順番に整列
        codeOrder = Util.Order.CATEGORY_ORDER
        for code in codeOrder :
            sortedCategories[code] = {}
            sortedCategories.move_to_end(code)

        ## 製品を格納
        for category in categories.items() :
            key = category[0]
            if (key not in sortedCategories) :
                ## 初見の場合は末尾に追加
                sortedCategories[key] = {}
                sortedCategories.move_to_end(key)
            sortedCategories[key][category[0]] = category[1]

        ## 一覧を出力
        productList = '-LIST-PRODUCT\n\n'
        totalNumberOfItems = 0;
        totalCost = 0;
        for category in sortedCategories.items() :
            productList += '- {} ------------------\n'.format(category[0].ljust(4))
            for orders in sorted(category[1].values()) :
                for order in orders :
                    unit = 0
                    if order[0] in Util.Order.BASE_PRODUCTION_COST :
                        unit = Util.Order.BASE_PRODUCTION_COST[order[0]]
                    else :
                        continue
                    cost = order[1] * unit
                    totalCost += cost
                    productList += '   {} : {} : {}\n'.format(order[0].ljust(10),
                                                              str(order[1]).rjust(2),
                                                              str(cost).rjust(6))
                    totalNumberOfItems += order[1]
            productList += '\n'

        productList += 'TOTAL : ' + str(totalNumberOfItems) + ' : ' + str(totalCost) + '\n'
        print(productList)

        dateTimeNow = datetime.now()
        fileName = dateTimeNow.strftime('%y%m%d%h%m%s')
        filePath = 'OrderLists/product_' + fileName + '.txt'
        with open(filePath, 'w') as f :
            f.write(productList)
            os.chmod(filePath, 0o777)


    ## 注文を追加（IDが既に存在する場合はエラー終了）


    ## 注文を取得


## 注文項目
class OrderItem :
    def __init__(self, aIdentifier, aStatus,
                 aAddressLine0, aAddressLine1, aCustomerName) :
        self.identifier   = aIdentifier   ## 注文ID
        self.status       = aStatus       ## 注文状況
        self.addressLine0 = aAddressLine0 ## 都道府県市区町村番地
        self.addressLine1 = aAddressLine1 ## 建物名部屋番号等
        self.customerName = aCustomerName ## 氏名
        self.products     = []            ## 商品（複数）


    ## 商品を追加
    def addProduct(self, aProduct) :
        print ("CALLED : addProduct(" + aProduct + ")");
        self.products.append(aProduct)

