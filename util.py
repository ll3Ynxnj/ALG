import re
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


        ## 注文データ種別コード
        class Format(Enum) :
            OTHER = 0
            MINNE = 1
            CREEMA = 2

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
        HEADER_PRINTING_LABELS = 'ラベルID,都道府県市区町村番地,建物名部屋番号等,氏名,商品,メモ'

        ## 注文の項目名からデータ種別を判定
        @staticmethod
        def getCsvFormat(aFile) :
            header = aFile.read().split('\n')[0]
            if (Util.Csv.HEADER_MINNE in header) :
                print ('DETECTED : CSV for minne')
                return Util.Order.Format.MINNE
            elif (Util.Csv.HEADER_CREEMA_0 in header or
                  Util.Csv.HEADER_CREEMA_1 in header) :
                print ('DETECTED : CSV for creema')
                return Util.Order.Format.CREEMA
            elif (Util.Csv.HEADER_PRINTING_LABELS in header) :
                print ('DETECTED : CSV for printing labels')
                return Util.Order.Format.PRINTING_LABELS
            else :
                print ('DETECTED : UNKNOWN')
                return Util.Order.Format.OTHER

