import re
import sys
from datetime import datetime
from enum import Enum

class Util :
    ## 注文ユーティリティ
    class Order :
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
            '00' : '0',
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
            '00',
        ]


        ## 注文データ種別コード
        class Format(Enum) :
            OTHER = 0
            MINNE = 1
            CREEMA = 2
            MANUAL_INPUT = 64
            PRINTING_LABELS = 256 

            NONE = -1


        ## 注文状況コード
        class ItemStatus(Enum) :
            NOT_PAYMENT = 0
            WAITING_FOR_SHIPPING = 1
            SHIPPED = 2
            CANCELED = 3

            NONE = -1


        ## 文字列から注文状況コードを取得
        @staticmethod
        def getStatus(aStatus) :
            orderItemStatus = Util.Order.ItemStatus.NONE
            return orderItemStatus


        ## 種別コードからデフォルトコードを取得
        @staticmethod
        def getDefaultCode(aCategoryCode) :
            return aCategoryCode + '-' + Util.Order.DEFAULT_OPTIONS[aCategoryCode]


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
            print ('CALLED : getProductCode({})'.format(aString))
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
            categoryCode = Util.Order.getCategoryCode(productCode)
            defaultCode = Util.Order.getDefaultCode(categoryCode)
            print ('defaultCode : ' + defaultCode)
            if defaultCode in productCode :
                productCode = productCode.replace(defaultCode, '')
                if productCode :
                    if productCode[0] != '-' :
                        productCode = '-' + productCode
                productCode = categoryCode + productCode
            productCode += otherCode

            return productCode


    ## CSVユーティリティ
    class Csv :
        #CSV_HEADER_MINNE = '注文ID,注文日'
        HEADER_MINNE = '注文ID,注文日,注文状況,支払方法,入金確認日,発送日,作品名,配送方法,配送エリア,発送までの目安,販売価格,数量,小計,備考,注文の販売価格,注文の送料,注文の合計,注文者のユーザーID,注文者のニックネーム,注文者の氏名,注文者の電話番号,配送先の郵便番号,配送先の住所1,配送先の住所2,配送先の氏名,配送先の電話番号,作品管理番号'
        #CSV_HEADER_CREEMA = '注文ID,購入日'
        HEADER_CREEMA_0 = '注文ID,購入日,ステータス,支払い日,発送予定日,発送日,作品タイトル,作品単価,オプション1,オプション1価格,オプション2,オプション2価格,作品価格,数量,ギフトラッピング,備考,取引相手,購入回数,配送方法,配送料,作品合計,送料・ラッピング,(-)作家クーポン,合計金額,(-)ポイント・お買い物券利用分,ご注文金額,氏名,郵便番号,住所,TEL,ナビURL,メモ,最終更新日'
        HEADER_CREEMA_1 = '注文ID,購入日,ステータス,支払い日,発送予定日,発送日,作品タイトル,作品単価,オプション1,オプション1価格,オプション2,オプション2価格,作品価格,数量,ギフトラッピング,備考,取引相手,購入回数,配送方法,配送料,作品合計,送料・ラッピング,(-)作家クーポン,合計金額,(-)お買い物券・ポイント・キャンペーン分,ご注文金額,氏名,郵便番号,住所,TEL,ナビURL,メモ,最終更新日'
        HEADER_MANUAL_INPUT = '注文ID,住所0,住所1,氏名,電話番号,商品,メモ'

        HEADER_PRINTING_LABELS = 'ラベルID,宛先0,宛先1,宛名,商品,差出人,メモ'

        ## 注文の項目名からデータ種別を判定
        @staticmethod
        # TODO Rename to 'getFormat'
        # TODO Create class 'Util.Csv.Format'
        def getCsvFormat(aFile) :
            header = aFile.read().split('\n')[0]
            if (Util.Csv.HEADER_MINNE in header) :
                print ('DETECTED : CSV for minne')
                return Util.Order.Format.MINNE
            elif (Util.Csv.HEADER_CREEMA_0 in header or
                  Util.Csv.HEADER_CREEMA_1 in header) :
                print ('DETECTED : CSV for creema')
                return Util.Order.Format.CREEMA
            elif (header == Util.Csv.HEADER_MANUAL_INPUT) :
                print ('DETECTED : CSV for manual input')
                return Util.Order.Format.MANUAL_INPUT
            elif (header == Util.Csv.HEADER_PRINTING_LABELS) :
                print ('DETECTED : CSV for printing labels')
                return Util.Order.Format.PRINTING_LABELS
            else :
                print ('DETECTED : UNKNOWN')
                return Util.Order.Format.OTHER

    ##
    class Text :
        class Format(Enum) :
            OTHER = 0
            ORDER_MINNE = 1
            ORDER_CREEMA = 2
            LABEL = 100
            LIST_CUSTOMER = 301
            LIST_PRODUCT = 302

            NONE = -1

        HEADER_ORDER_MINNE = '-ORDER-M\n'
        HEADER_ORDER_CREEMA = '-ORDER-C\n'
        HEADER_LABEL = '-LABEL\n'
        HEADER_LIST_CUSTOMER = '-LIST-CUSTOMER\n'
        HEADER_LIST_PRODUCT = '-LIST-PRODUCT\n'


        @staticmethod
        def getFormat(aFile) :
            aFile.seek(0, 0)
            header = aFile.readline()
            print('Header : ' + header.split('\n')[0])
            if (Util.Text.HEADER_ORDER_MINNE == header) :
                print ('DETECTED : Text with orders for minne')
                return Util.Text.Format.ORDER_MINNE
            elif (Util.Text.HEADER_ORDER_CREEMA == header) :
                print ('DETECTED : Text with orders for creema')
                return Util.Text.Format.ORDER_CREEMA
            elif (Util.Text.HEADER_LABEL == header) :
                print ('DETECTED : Text for label printing')
                return Util.Text.Format.LABEL
            elif (Util.Text.HEADER_LIST_CUSTOMER == header) :
                print ('DETECTED : Text for customer list')
                return Util.Text.Format.LIST_CUSTOMER
            elif (Util.Text.HEADER_LIST_PRODUCT == header) :
                print ('DETECTED : Text for product list')
                return Util.Text.Format.LIST_PRODUCT
            else :
                print ('DETECTED : UNKNOWN')
                return Util.Text.Format.OTHER


        @staticmethod
        def getCsvBodyWithFile(aFile) :
            return csvBody


        @staticmethod
        def genCsvWithFileForMinne(aFile) :
            print('CALLED : genCsvWithFileForMinne()')
            aFile.seek(0, 0)
            lines = aFile.read().split('\n')
            length = len(lines)
            csv = Util.Csv.HEADER_MANUAL_INPUT + '\n'
            headerWidth = 2
            dataWidth = 7
            if length % dataWidth != headerWidth :
                print ('ERROR : Invalid file length.')
                sys.exit(1)
            now = datetime.now()
            strNow = now.strftime('%Y%m%d-%H%M%S-%f')
            filename = 'order-mi-{:s}'.format(strNow)
            numData = int((length - headerWidth) / dataWidth)
            for i in range(numData) :
                head = headerWidth + i * dataWidth
                tail = head + dataWidth
                data = lines[head:tail]
                print ('lines : ' + str(data[dataWidth - 1]))
                if len(data[dataWidth - 1]) :
                    print ('ERROR : Detected unexpected data.')
                    sys.exit(1)
                identifier = filename + '-{:06d}'.format(i)
                name = data[0]
                address0 = data[1]
                address1 = data[2]
                phoneNumber = data[3]
                products = data[4].upper().split('/')
                print('products : {}'.format(products))
                memo = data[5]
                for product in products :
                    productCode = ''
                    for item in product.split() :
                        productCode += '[' + item + ']'
                    print('productCode : ', productCode)
                    rowData = (identifier, address0, address1, name, phoneNumber, productCode, memo)
                    csv += Util.Text.getCsvRow(rowData, ',')
            print('-- CSV generated -------------------------------------------')
            print(csv)
            print('------------------------------------------------------------')
            filepath = 'DataSource/' + filename + '.csv'
            with open(filepath, 'w') as f:
                print(csv, file = f)


        @staticmethod
        def genCsvWithFileForCreema(aFile) :
            print('CALLED : genCsvWithFileForMinne()')
            aFile.seek(0, 0)
            lines = aFile.read().split('\n')
            length = len(lines)
            print('length : ' + str(length))
            print(lines)
            csv = Util.Csv.HEADER_MANUAL_INPUT + '\n'
            headerWidth = 2
            dataWidth = 5
            if (length % dataWidth) != headerWidth :
                print ('ERROR : Invalid file length.')
                sys.exit(1)
            now = datetime.now()
            strNow = now.strftime('%Y%m%d-%H%M%S-%f')
            filename = 'order-cr-{:s}'.format(strNow)
            numData = int((length - headerWidth) / dataWidth)
            for i in range(numData) :
                head = headerWidth + i * dataWidth
                tail = head + dataWidth
                data = lines[head:tail]
                if len(data[dataWidth - 1]) :
                    print ('ERROR : Detected unexpected data.')
                    sys.exit(1)
                identifier = filename + '-{:06d}'.format(i)
                postalCode = data[0][0:7]
                if not postalCode.isdecimal() :
                    print ('ERROR : postalCode : {} : It is not decimal.'.format(postalCode))
                    sys.exit(1)
                name = data[1]
                address0 = '〒' + postalCode[0:3] + '-' + postalCode[3:]
                address1 = data[0][7:]
                phoneNumber = ''
                products = data[2].upper().split('/')
                memo = data[3]
                print('products : {}'.format(products))
                for product in products :
                    productCode = ''
                    items = product.split()
                    for item in items :
                        productCode += '[' + item + ']'
                    print('productCode : ', productCode)
                    rowData = (identifier, address0, address1, name, phoneNumber, productCode, memo)
                    csv += Util.Text.getCsvRow(rowData, ',')
            print('-- CSV generated -------------------------------------------')
            print(csv)
            print('------------------------------------------------------------')
            filepath = 'DataSource/' + filename + '.csv'
            with open(filepath, 'w') as f:
                print(csv, file = f)


        def genCsvWithFileForLabel(aFile):
            print('CALLED : genCsvWithFileForLabel()')
            aFile.seek(0, 0)
            lines = aFile.read().split('\n')
            length = len(lines)
            csv = Util.Csv.HEADER_PRINTING_LABELS + '\n'
            headerWidth = 2
            dataWidth = 8
            if length % dataWidth != headerWidth:
                print ('ERROR : Invalid file length.')
                sys.exit(1)
            now = datetime.now()
            strNow = now.strftime('%Y%m%d-%H%M%S-%f')
            filename = 'label-{:s}'.format(strNow)
            numData = int((length - headerWidth) / dataWidth)
            for i in range(numData):
                head = headerWidth + i * dataWidth
                tail = head + dataWidth
                data = lines[head:tail]
                print ('lines : ' + str(data[dataWidth - 1]))
                if len(data[dataWidth - 1]):
                    print ('ERROR : Detected unexpected data.')
                    sys.exit(1)
                identifier = filename + '-{:06d}'.format(i)
                address0 = data[0]
                address1 = data[1]
                name = data[2]
                products = data[3]
                fromAddress = data[4]
                quantity = int(data[5])
                memo = data[6]
                for j in range(quantity):
                    labelIdentifier = identifier + '-{:06d}'.format(j)
                    rowData = (labelIdentifier, address0, address1, name, products, fromAddress, memo)
                    csv += Util.Text.getCsvRow(rowData, ',')
            print('-- CSV generated -------------------------------------------')
            print(csv)
            print('------------------------------------------------------------')
            filepath = 'DataSource/' + filename + '.csv'
            with open(filepath, 'w') as f:
                print(csv, file = f)


        @staticmethod
        def getCsvRow(aRowData, aDelimiter) :
            csvRow = ''
            for column in aRowData :
                csvRow += '"' + str(column).replace('"', "") + '"' + aDelimiter
            csvRow += '\n'
            return csvRow
