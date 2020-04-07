# coding:utf-8

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import os
import webbrowser
import unicodedata

def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


class LabelGenerater() :
    def __init__(self) :
        self.page_size   = (90*mm,29*mm) # 90x29mm
        self.font_family = 'GenShinGothic' # http://jikasei.me/font/genshin/
        self.font_path   = './fonts/GenShinGothic-Monospace-Medium.ttf'

    def genLabel(self, aOrderItem) :
        # カンバス作成
        label_path  = 'Labels/' + aOrderItem.identifier + '.pdf'
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
        context.drawString(margin_1, height - margin_1 - font_size_m,
                           aOrderItem.addressLine0)

        # アドレスが長すぎる場合はフォントサイズを縮小
        font_size_AL1 = font_size_m
        length_AL1 = get_east_asian_width_count(aOrderItem.addressLine1)
        resize_ratio_AL1 = 53.1 / length_AL1
        if resize_ratio_AL1 < 1.0 :
            font_size_AL1 *= resize_ratio_AL1
        context.setFont(self.font_family, font_size_AL1)
        context.drawString(margin_1, height - margin_1 - font_size_m - font_size_m * 1.17,
                           aOrderItem.addressLine1)

        context.setFont(self.font_family, font_size_l)
        context.drawString(margin_1, 12.65*mm,
                           aOrderItem.customerName + ' 様')

        productStr = '';
        for product in aOrderItem.products :
            productStr += product + ' '

        context.setFont(self.font_family, font_size_s)
        context.drawString(margin_1, 6.82*mm, productStr)

        context.setLineWidth(0.14*mm)
        context.line(margin_1, 5.81*mm, width - margin_1, 5.81*mm)

        context.setFont(self.font_family, 3.15*mm)
        context.drawString(margin_1, margin_1,
                           'Aikiki 〒227-0038神奈川県横浜市青葉区奈良3-14-1-八-908')

        context.showPage()

        # ファイル保存
        context.save()
        os.chmod(label_path, 0o777)

#        # 回転
#        PDF = label_path #入力ファイル名
#        OutputName = 'TEST_Rotated/' + label_path #出力ファイル名
#        angle = 270 #回転角度
#
#        File = open(PDF, 'rb')
#        Reader = PyPDF2.PdfFileReader(File)
#        Writer = PyPDF2.PdfFileWriter()
#        for page in range(Reader.numPages):
#            obj = Reader.getPage(page)
#            obj.rotateClockwise(angle)
#            Writer.addPage(obj)
#
#        Output = open(OutputName, 'wb')
#        Writer.write(Output)
#        Output.close()
#        File.close()
