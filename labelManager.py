# coding:utf-8

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import os
import csv
import sys
import unicodedata

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


class LabelManager :
    def __init__(self) :
        self.page_size   = (90*mm,29*mm) # 90x29mm
        self.font_family = 'GenShinGothic' # http://jikasei.me/font/genshin/
        self.font_path   = './fonts/GenShinGothic-Monospace-Medium.ttf'
        self.items       = list()


    def genLabel(self) :
        for item in self.items :
            self.genLabelWithItem(item)


    def genLabelWithItem(self, aLabelItem) :
        identifier   = aLabelItem.identifier
        addressLine0 = aLabelItem.addressLine0
        addressLine1 = aLabelItem.addressLine1
        customerName = aLabelItem.customerName
        products     = aLabelItem.products
        fromAddress  = aLabelItem.fromAddress

        # カンバス作成
        if not len(identifier) :
            print('ERROR : Identifier is undefined.')
            sys.exit()
        label_path  = 'Labels/' + identifier + '.pdf'
        context = canvas.Canvas(label_path, landscape(self.page_size))

        # フォント登録
        pdfmetrics.registerFont(TTFont(self.font_family, self.font_path))

        # ラベル描画
        font_size_ss = 1.98*mm
        font_size_s = 2.60*mm
        font_size_m = 3.21*mm
        font_size_l = 5.20*mm
        margin_0 = 1.60*mm
        margin_1 = 2.60*mm
        width, height = self.page_size # 90x29mm

        context.setFont(self.font_family, font_size_m)
        context.drawString(margin_1,
                           height - margin_1 - font_size_m,
                           addressLine0)# アドレスが長すぎる場合はフォントサイズを縮小
        font_size_AL1 = font_size_m
        length_AL1 = get_east_asian_width_count(addressLine1)
        if length_AL1 == 0 :
            length_AL1 = 1;
        resize_ratio_AL1 = 53.1 / length_AL1
        if resize_ratio_AL1 < 1.0 :
            font_size_AL1 *= resize_ratio_AL1
        context.setFont(self.font_family, font_size_AL1)
        context.drawString(margin_1,
                           height - margin_1 - font_size_m - font_size_m * 1.17,
                           addressLine1)

        context.setFont(self.font_family, font_size_l)
        context.drawString(margin_1, 12.65*mm, customerName)

        context.setFont(self.font_family, font_size_s)
        context.drawString(margin_1, 6.82*mm, products)

        context.setLineWidth(0.14*mm)
        context.line(margin_1, 5.81*mm, width - margin_1, 5.81*mm)

        context.setFont(self.font_family, 3.15*mm)
        context.drawString(margin_1, margin_1, fromAddress)

        context.showPage()

        # ファイル保存
        context.save()
        os.chmod(label_path, 0o777)


    def addItemWithOrder(self, aOrderItem) :
        print('CALLED : addItemWithOrder(self, {})'.format(aOrderItem))
        identifier = aOrderItem.identifier
        if identifier == '' :
            print('ERROR : Identifier is undefined.')
            sys.exit()
        addressLine0 = aOrderItem.addressLine0
        addressLine1 = aOrderItem.addressLine1
        customerName = aOrderItem.customerName + ' 様'
        products = ''
        for product in aOrderItem.products :
            products += product + ' '
        fromAddress = 'Aikiki 〒227-0038神奈川県横浜市青葉区奈良3-14-1-八-908'

        item = LabelItem(identifier,
                         addressLine0,
                         addressLine1,
                         customerName,
                         products,
                         fromAddress)
        self.items.append(item)
        print('item : {} {}'.format(item.identifier, item.customerName))


    def addItemWithFile(self, aFilename) :
        print('CALLED : addItemWithFile()')
        with open(aFilename, 'r', encoding='utf-8-sig') as filedata :
            print ("OPENED : " + aFilename)
            csvDict = csv.DictReader(filedata)

            for row in csvDict :
                item = LabelItem(row['ラベルID'],
                                 row['宛先0'],
                                 row['宛先1'],
                                 row['宛名'],
                                 row['商品'],
                                 row['差出人'])
                self.items.append(item)
                print('item : {} {}'.format(item.identifier, item.customerName))


## ラベル項目
class LabelItem :
    def __init__(self, aIdentifier,
                 aAddressLine0, aAddressLine1, aCustomerName,
                 aProducts, aFromAddress) :
        self.identifier   = aIdentifier   ## ラベルID
        self.addressLine0 = aAddressLine0 ## 都道府県市区町村番地
        self.addressLine1 = aAddressLine1 ## 建物名部屋番号等
        self.customerName = aCustomerName ## 氏名
        self.products     = aProducts     ## 商品
        self.fromAddress  = aFromAddress  ## 差出人
