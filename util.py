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
            'PP' : 'G',
            'PSRE' : 'G',
            'PSDI' : 'G',
            'PSDR' : 'G',
            'PSLO' : 'G',
            'HD' : 'G',
            'HS' : 'G',
            'TH' : 'G',
            'WC' : 'G',
            'WCC' : 'G',
            'WCS' : 'G',
            'WCP' : 'G',
            'WCT' : 'G',
            'WD' : 'G',
            'WDS' : 'G',
            'OP' : 'G',
            'OT3' : 'GS',
            'OLA' : 'T',
            'OTA' : 'T',
            'OZF' : 'G',    # One Zirconia Flower
            'SM' : 'GT',    #旧JM
            'ST4' : 'GT',   #旧JT
            'KP' : 'G',
            'SP' : 'G',
    	    'SS' : 'G',
            'SPDI' : 'G',
            'KD' : 'G',
            'FC' : 'G',
            'ZF' : 'GH',    #旧JF
            'PD' : 'G',
            'PC' : 'G',
            'VS' : 'GH',
            'VB' : 'G',
            'ST' : 'GT',
            'LB' : 'G',
            'LQ' : 'GH',
            'AD' : 'GH',
            'WT' : 'GH',
            'FWT' : 'GH',
            'FSQ' : 'GH',
            'HFWT' : 'GH',
            'HC' : 'G',
            'DZA' : 'G',    #旧JA
            'DZS' : 'G',    #旧JS
            'DZT' : 'G',
            'CM' : 'GH',
            'FLA' : 'GH',
            'FTA' : 'GH',
            'FMO' : 'GH',
            'FGA' : 'GH',
            'CTA' : 'G',
            'PB' : 'G',
            'SCS' : 'G',
            'SCP' : 'G',
            'SK3' : 'G',
            'OST' : 'G',
            'OD' : 'S',
            'ST3' : 'S',
            'WCG' : 'G',
            'WCA' : 'G',
            'GA4' : 'G',
            'RTA' : 'G',
            'N:FOP': 'G40',
            'N:ZF': 'G40',  #旧N:FJF
            'N:FWT': 'G40',
            'N:LB' : 'G40',
            'N:MG' : 'G40',
            'N:WT' : 'G40',
            'N:SK3' : 'G45',
            'R:ST' : '==ERROR==',
            'R:GO' : '==ERROR==',
            'R:ZR2' : '==ERROR==',
            'R:FOW' : '==ERROR==',
            'R:TIE' : '==ERROR==',
            'B:CD' : '==ERROR==',
            '00' : '0',
        }


        CATEGORY_ORDER = [
            'PK',
            'PS',
            'PP',    # Pearl Pearl
            'PSRE',
            'PSDI',
            'PSDR',
            'PSLO',
            'HD',    # Herkimer-Diamond Drop (WDHが望ましい)
            'HS',    # Herkimer-Diamond Stick (WSHが望ましい）
            'TH',
            'WC',
            'WCC',   # Wired Circle Crystal
            'WCS',
            'WCP',
            'WCT',
            'WD',
            'WDS',
            'OP',
            'OT3',
            'OLA',
            'OTA',
            'OZF',   # One Zirconia Flower
            'SM',    # Swarovski #'JM',
            'ST4',   # Swarovski 淡水パール(T) 4連 #'JT',
            'KP',
            'KD',
            'SP',
            'SS',    # Swarovski Swarovski
            'SPDI',
            'FC',
            'ZF',    # Zirconia Flower #'JF',
            'PD',
            'PC',
            'VS',
            'VB',
            'ST',    # Swarovski 淡水パール(T)
            'LB',
            'LQ',
            'AD',    # Amazonite Drop
            'WT',
            'FWT',
            'FSQ',   # Framed Smoky Quartz
            'HFWT',
            'HC',    # Hoop Circle
            'DZA',   # Drop Zirconia Amazonite #'JA'
            'DZS',   # Drop Zirconia Swarovski #'JS'
            'DZT',   # Drop Zirconia 淡水パール(T)
            'CM',
            'FLA',
            'FTA',
            'FMO',
            'FGA',
            'CTA',
            'ST3',
            'PB',
            'SCS',
            'SCP',
            'SK3',
            'OST',
            'OD',    # One Designe (<-?)
            'WCG',
            'WCA',
            'GA4',
            'RTA',
            'N:FOP',
            'N:ZF',  # Zirconia Flower #'N:FJF',
            'N:FWT',
            'N:LB',
            'N:MG',
            'N:WT',
            'N:SK3', # Stick Crystal 3
            'R:ST',
            'R:GO',  # Green Onikis
            'R:ZR2', # Zirconia Round 2mm
            'R:FOW', # Framed Oval Wave
            'R:TIE', # Tie
            'B:CD',  # Chain Dot
            '00',
        ]


        BASE_PRODUCTION_COST = {
            'PK' : 450,
            'PK-J' : 450,
            'PK-N' : 450,
            'PK-B' : 450,
            'PS' : 450,
            'PS-J' : 450,
            'PS-N' : 450,
            'PS-B' : 450,
            'PS-S' : 450,
            'PS-SJ' : 450,
            'PS-SN' : 450,
            'PS-SB' : 450,
            'KP' : 450,
            'KP-J' : 450,
            'KP-N' : 450,
            'KP-B' : 450,
            'KP-T' : 450,
            'KP-E' : 450,
            'KP-S' : 450,
            'KP-SJ' : 450,
            'KP-SN' : 450,
            'KP-SB' : 450,
            'KP-ST' : 450,
            'KP-SE' : 450,
            'SP' : 450,
            'SP-J' : 450,
            'SP-N' : 450,
            'SP-B' : 450,
            'SP-T' : 450,
            'SP-E' : 450,
            'SP-S' : 450,
            'SP-SJ' : 450,
            'SP-SN' : 450,
            'SP-SB' : 450,
            'SP-ST' : 450,
            'SP-SE' : 450,
            'SPDI' : 450,
            'SPDI-J' : 450,
            'SPDI-N' : 450,
            'SPDI-B' : 450,
            'SPDI-T' : 450,
            'SPDI-S' : 450,
            'SPDI-SJ' : 450,
            'SPDI-SN' : 450,
            'SPDI-SB' : 450,
            'SPDI-ST' : 450,
            'HD' : 1000,
            'HD-J' : 1000,
            'HD-N' : 1000,
            'HD-B' : 1000,
            'HD-S' : 1000,
            'HD-SJ' : 1000,
            'HD-SN' : 1000,
            'HD-SB' : 1000,
            'TH' : 750,
            'TH-N' : 750,
            'TH-S' : 750,
            'TH-SN' : 750,
            'WC' : 450,
            'WC-N' : 550,
            'WC-B' : 450,
            'WC-S' : 450,
            'WC-SN' : 550,
            'WC-SB' : 450,
            'WD' : 450,
            'WD-N' : 550,
            'WD-B' : 450,
            'WD-S' : 450,
            'WD-SN' : 550,
            'WD-SB' : 450,
            'WCS' : 500,
            'WCS-N' : 600,
            'WCS-B' : 500,
            'WCS-S' : 500,
            'WCS-SN' : 600,
            'WCS-SB' : 500,
            'WDS' : 500,
            'WDS-N' : 600,
            'WDS-B' : 500,
            'WDS-S' : 500,
            'WDS-SN' : 600,
            'WDS-SB' : 500,
            'WCP' : 550,
            'WCP-N' : 650,
            'WCP-B' : 550,
            'WCP-S' : 550,
            'WCP-SN' : 650,
            'WCP-SB' : 550,
            'WCT' : 550,
            'WCT-N' : 650,
            'WCT-B' : 550,
            'WCT-S' : 550,
            'WCT-SN' : 650,
            'WCT-SB' : 550,                
            'WCA' : 450, # WC 
            'WCG' : 450, # WC
            'WCC' : 450, # WC
        }


        ## 注文データ種別コード
        class Format(Enum) :
            OTHER = 0
            MINNE = 1
            CREEMA = 2
            BASE = 3
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
        HEADER_CREEMA_2 = '注文ID,購入日,ステータス,支払い日,発送予定日,発送日,作品タイトル,種類,作品単価,オプション1,オプション1価格,オプション2,オプション2価格,オプション3,オプション3価格,オプション4,オプション4価格,オプション5,オプション5価格,作品価格,数量,ギフトラッピング,備考,取引相手,購入回数,配送方法,配送料,作品合計,送料・ラッピング,(-)作家クーポン,合計金額,(-)お買い物券・ポイント・キャンペーン分,ご注文金額,氏名,郵便番号,住所,TEL,ナビURL,メモ,最終更新日'
        HEADER_CREEMA_SALES = '"購入日","確定日","取引相手","作品タイトル","作品URL","種類","作品単価","オプション1","オプション1価格","オプション2","オプション2価格","オプション3","オプション3価格","オプション4","オプション4価格","オプション5","オプション5価格","作品価格","数量","作品合計","ポイント利用分（振込み予定金額の計算には含まれません）","キャンペーン還元率（%）","(-)キャンペーン適用合計","(-)クーポン適用分","(-)成約手数料","(+)送料","(+)ラッピング","売上金（広告費控除前）","振込申請日"'
        HEADER_BASE = '注文ID,注文日時,氏(請求先),名(請求先),郵便番号(請求先),都道府県(請求先),住所(請求先),住所2(請求先),電話番号(請求先),メールアドレス(請求先),氏(配送先),名(配送先),郵便番号(配送先),都道府県(配送先),住所(配送先),住所2(配送先),電話番号(配送先),備考,商品名,バリエーション,価格,税率,数量,合計金額,送料,支払い方法,代引き手数料,発送状況,商品ID,種類ID,購入元,配送日,配送時間帯,注文メモ,調整金額'
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
                  Util.Csv.HEADER_CREEMA_1 in header or
                  Util.Csv.HEADER_CREEMA_2 in header or
                  Util.Csv.HEADER_CREEMA_SALES in header) :
                print ('DETECTED : CSV for Creema')
                return Util.Order.Format.CREEMA
            elif (Util.Csv.HEADER_BASE in header) :
                print ('DETECTED : CSV for BASE')
                return Util.Order.Format.BASE
            elif (header == Util.Csv.HEADER_MANUAL_INPUT) :
                print ('DETECTED : CSV for manual input')
                return Util.Order.Format.MANUAL_INPUT
            elif (header == Util.Csv.HEADER_PRINTING_LABELS) :
                print ('DETECTED : CSV for printing labels')
                return Util.Order.Format.PRINTING_LABELS
            else :
                print ('DETECTED : UNKNOWN')
                print ('-- HEADER --')
                print (header)
                print ('------------')
                return Util.Order.Format.OTHER


    ##
    class Text :
        class Format(Enum) :
            OTHER = 0
            ORDER_MINNE = 1
            ORDER_CREEMA = 2
            ORDER_BASE = 3
            LABEL = 100
            LIST_CUSTOMER = 301
            LIST_PRODUCT = 302

            NONE = -1

        HEADER_ORDER_MINNE = '-ORDER-M\n'
        HEADER_ORDER_CREEMA = '-ORDER-C\n'
        HEADER_ORDER_BASE = '-ORDER-B\n'
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
                print ('DETECTED : Text with orders for Creema')
                return Util.Text.Format.ORDER_CREEMA
            elif (Util.Text.HEADER_ORDER_BASE== header) :
                print ('DETECTED : Text with orders for BASE')
                return Util.Text.Format.ORDER_BASE
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
        def genCsvWithFileForMinne(aFile) :
            print('CALLED : genCsvWithFileForMinne()')
            aFile.seek(0, 0)
            text = aFile.read().rstrip() + '\n'
            lines = text.split('\n')
            length = len(lines)
            print('length : ' + str(length))
            print(lines)
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
            print('CALLED : genCsvWithFileForCreema()')
            aFile.seek(0, 0)
            text = aFile.read().rstrip() + '\n'
            lines = text.split('\n')
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


        @staticmethod
        def genCsvWithFileForLabel(aFile):
            print('CALLED : genCsvWithFileForLabel()')
            aFile.seek(0, 0)
            text = aFile.read().rstrip() + '\n'
            lines = text.split('\n')
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
