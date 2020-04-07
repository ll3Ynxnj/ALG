# coding:utf-8

import os
import re
import csv
import pprint
import collections
from datetime import datetime
from enum import Enum

## 注文データ種別コード
class CsvFormat(Enum) :
    OTHER = 0
    MINNE = 1
    CREEMA = 2

    NONE = -1

## 注文状況コード
class OrderItemStatus(Enum) :
    NOT_PAYMENT = 0
    WAITING_FOR_SHIPPING = 1
    SHIPPED = 2
    CANCELED = 3

    NONE = -1

## デフォルトオプション
DEFAULT_OPTIONS = {
    'PK' : 'G',
    'PS' : 'G',
    'HD' : 'G',
    'TH' : 'G',
    'WCS' : 'G',
    'WCP' : 'G',
    'WCT' : 'G',
    'WDS' : 'G',
    'OP' : 'G',
    'OLA' : 'T',
    'OTA' : 'T',
    'KP' : 'G',
    'SP' : 'G',
    'KD' : 'G',
    'FC' : 'G',
    'JT' : 'GT',
    'JM' : 'GT',
    'JF' : 'GF',
    'PD' : 'G',
    'PC' : 'G',
    'VS' : 'GF',
    'VB' : 'G',
    'ST' : 'GT',
    'LB' : 'G',
    'WT' : 'GF',
    'CM' : 'GF',
    'LA' : 'GF',
    'TA' : 'GF',
    'PB' : 'G',
    'SS' : 'G',
    'WCG' : 'G',
    'WCA' : 'G',
    'RTA' : 'G',
    'N:LB' : 'G40',
    'N:MG' : 'G40',
    'N:WT' : 'G40',
    'R:ST' : '==ERROR==',
}

CATEGORY_ORDER = [
    'PK',
    'PS',
    'HD',
    'TH',
    'WCS',
    'WCP',
    'WCT',
    'WDS',
    'OP',
    'OLA',
    'OTA',
    'KP',
    'KD',
    'SP',
    'FC',
    'JT',
    'JM',
    'JF',
    'PD',
    'PC',
    'VS',
    'VB',
    'ST',
    'LB',
    'WT',
    'CM',
    'LA',
    'TA',
    'PB',
    'SS',
    'WCG',
    'WCA',
    'RTA',
    'N:LB',
    'N:MG',
    'N:WT',
    'R:ST',
]

#CSV_HEADER_MINNE = '注文ID,注文日'
CSV_HEADER_MINNE = '注文ID,注文日,注文状況,支払方法,入金確認日,発送日,作品名,配送方法,配送エリア,発送までの目安,販売価格,数量,小計,備考,注文の販売価格,注文の送料,注文の合計,注文者のユーザーID,注文者のニックネーム,注文者の氏名,注文者の電話番号,配送先の郵便番号,配送先の住所1,配送先の住所2,配送先の氏名,配送先の電話番号,作品管理番号'
#CSV_HEADER_CREEMA = '注文ID,購入日'
CSV_HEADER_CREEMA_0 = '注文ID,購入日,ステータス,支払い日,発送予定日,発送日,作品タイトル,作品単価,オプション1,オプション1価格,オプション2,オプション2価格,作品価格,数量,ギフトラッピング,備考,取引相手,購入回数,配送方法,配送料,作品合計,送料・ラッピング,(-)作家クーポン,合計金額,(-)ポイント・お買い物券利用分,ご注文金額,氏名,郵便番号,住所,TEL,ナビURL,メモ,最終更新日'
CSV_HEADER_CREEMA_1 = '注文ID,購入日,ステータス,支払い日,発送予定日,発送日,作品タイトル,作品単価,オプション1,オプション1価格,オプション2,オプション2価格,作品価格,数量,ギフトラッピング,備考,取引相手,購入回数,配送方法,配送料,作品合計,送料・ラッピング,(-)作家クーポン,合計金額,(-)お買い物券・ポイント・キャンペーン分,ご注文金額,氏名,郵便番号,住所,TEL,ナビURL,メモ,最終更新日'

## 注文ユーティリティ
class OrderUtility :
    ## 注文の項目名からデータ種別を判定
    @staticmethod
    def getCsvFormat(aFile) :
        header = aFile.read().split('\n')[0]
        if (CSV_HEADER_MINNE in header) :
            print ('DETECTED : CSV for minne')
            return CsvFormat.MINNE
        elif (CSV_HEADER_CREEMA_0 in header or
              CSV_HEADER_CREEMA_1 in header) :
            print ('DETECTED : CSV for creema')
            return CsvFormat.CREEMA
        else :
            print ('DETECTED : UNKNOWN')
            return CsvFormat.OTHER


    ## 文字列から注文状況コードを取得
    @staticmethod
    def getStatus(aStatus) :
        orderItemStatus = OrderItemStatus.NONE
        return orderItemStatus


    ## 種別コードからデフォルトコードを取得
    @staticmethod
    def getDefaultCode(aCategoryCode) :
        return aCategoryCode + '-' + DEFAULT_OPTIONS[aCategoryCode]


    ## 商品コードから種別コードを取得
    @staticmethod
    def getCategoryCode(aProductCode) :
        i = aProductCode.find('-')
        if (i == -1) :
            i = len(aProductCode)
        return aProductCode[0:i]


    ## 文字列から商品コードを取得
    @staticmethod
    def getProductCode(aString) :
        productCode = ''
        items = re.findall('\[[a-zA-Z0-9\-:]*\]', aString)
        for item in items :
            if (productCode != '') :
                productCode += '-'
            productCode += item

        ## 数値、B、Wを末尾に移動、商品名にオプションが含まれていない場合は追加
        otherCode = '';
        if re.findall('-\[[0-9]*\]', productCode) :
            m = re.search(r'-\[[0-9]*\]', productCode)
            otherCode += m.group(0)
            productCode = re.sub('-\[[0-9]*\]', '', productCode)
        if '-[B]' in productCode :
            otherCode += '[-B]'
            productCode = productCode.replace('-[B]', '')
        if '-[W]' in productCode :
            otherCode += '[-W]'
            productCode = productCode.replace('-[W]', '')

        ## []を除去
        productCode = productCode.replace('[', '')
        productCode = productCode.replace(']', '')
        otherCode = otherCode.replace('[', '')
        otherCode = otherCode.replace(']', '')

        ## デフォルト値の場合はオプションを削除
        categoryCode = OrderUtility.getCategoryCode(productCode)
        defaultCode = OrderUtility.getDefaultCode(categoryCode)
        print ('defaultCode : ' + defaultCode)
        if defaultCode in productCode :
            productCode = productCode.replace(defaultCode, '')
            if productCode :
                if productCode[0] != '-' :
                    productCode = '-' + productCode
            productCode = categoryCode + productCode
        productCode += otherCode

        return productCode


## 注文マネージャー
class OrderManager :
    def __init__(self) :
        self.orders = collections.OrderedDict() # IDをキーとする注文辞書（重複不可）

    ## ファイルリストから注文を初期化
    def initOrders(self, aFileList) :
        self.orders.clear

        for filename in aFileList :
            with open(filename, 'r', encoding='utf-8-sig') as filedata:
                csvDictFormat = OrderUtility.getCsvFormat(filedata)
                if csvDictFormat == CsvFormat.MINNE :
                    self.addOrdersForMinne(filename)
                elif csvDictFormat == CsvFormat.CREEMA :
                    self.addOrdersForCreema(filename)
                else :
                    print('filename : ' + filename)
                    print('CSV形式が不明のため「' + filename + '」からは注文の追加ができませんでした')
                    sys.exit()


    ## 注文を追加（Minne）
    def addOrdersForMinne(self, aFilename) :
        print('CALLED : addOrdersForMinne()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)

            dbg_row = 0
            for row in csvDict :
                print (row)
                orderIdentifier = row['注文ID']

                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    orderItem = OrderItem(orderIdentifier,
                                          OrderUtility.getStatus(row['注文状況']),
                                          '〒' + row['配送先の郵便番号'],
                                          row['配送先の住所1'] + ' ' +
                                          row['配送先の住所2'],
                                          row['配送先の氏名'])
                    self.orders[orderIdentifier] = orderItem

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = OrderUtility.getProductCode(row['作品名'])

                for i in range(int(row['数量'])) :
                    orderItem.addProduct(productCode)

                # print(orderItem.products)
                ++dbg_row


    ## 注文を追加（Creema）
    def addOrdersForCreema(self, aFilename) :
        print('CALLED : addOrdersForCreema()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)
            dbg_row = 0
            for row in csvDict :
                print (row)
                orderIdentifier = row['注文ID']
                ## 注文を追加（既に存在する注文は纏める）
                isExist = orderIdentifier in self.orders.keys()
                if (isExist) :
                    ## ２件目以降の注文の場合は１件目で作成したオブジェクトを取得
                    orderItem = self.orders[orderIdentifier]
                else :
                    ## １件目の注文の場合はOrderItemを作成
                    postalCode = re.sub('[^0-9\-]', '', row['郵便番号'])
                    orderItem = OrderItem(orderIdentifier,
                                          OrderUtility.getStatus(row['ステータス']),
                                          '〒' + postalCode,
                                          row['住所'],
                                          row['氏名'])
                    self.orders[orderIdentifier] = orderItem

                productString = row['作品タイトル'] + row['オプション1'] + row['オプション2']
                ## Creemaのギフトラッピングはコードを振れないので「あり」の文字列を探して存在すれば追加
                if 'あり' in row['ギフトラッピング'] :
                    productString += '-[W]'

                ## 商品名から商品コードを抽出してOrderItemに追加
                print(aFilename + ' : row ' + str(dbg_row))
                productCode = OrderUtility.getProductCode(productString)

                for i in range(int(row['数量'])) :
                    orderItem.addProduct(productCode)

                # print(orderItem.products)
                ++dbg_row


    ## 注文を出力
    def printOrders(self) :
        print('CALLED : printOrders()')
        orderList = ''
        for order in self.orders.values() :
#            print ('--------')
#            print (order.identifier)
#            print (order.status)
#            print (order.addressLine0)
#            print (order.addressLine1)
#            print (order.customerName)
#            print (order.products)
            #orderList += '--------\n'
            orderList += str(order.identifier)
            #orderList += str(order.status)
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

        ## 出力
        #for order in sortedOrders :
        #    print ('{} : {}'.format(order[0].ljust(10), str(order[1]).rjust(2)));

        ## 製品名ごとに辞書を作成して出力
        categories = {};
        for order in sortedOrders : #sorted(orders.items()) :
            categoryCode = OrderUtility.getCategoryCode(order[0])
            if (categoryCode not in categories) :
                categories[categoryCode] = []
            categories[categoryCode].append(order)

        #sortedCategories = sorted(categories.items())

        sortedCategories = collections.OrderedDict()

        ## 順番に整列
        codeOrder = CATEGORY_ORDER
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
        productList = ''
        totalNumberOfItems = 0;
        for category in sortedCategories.items() :
            productList += '- {} ------------\n'.format(category[0].ljust(3))
            for orders in sorted(category[1].values()) :
                for order in orders :
                    productList += '   {} : {}\n'.format(order[0].ljust(10), str(order[1]).rjust(2))
                    totalNumberOfItems += order[1]
            productList += '\n'

        productList += 'TOTAL : ' + str(totalNumberOfItems)
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
