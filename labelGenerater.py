# coding:utf-8

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import webbrowser

class LabelGenerater() :
    def __init__(self) :
        self.page_size   = (90*mm,29*mm) # 90x29mm
        self.font_family = 'GenShinGothic' # http://jikasei.me/font/genshin/
        self.font_path   = './fonts/GenShinGothic-Monospace-Medium.ttf'

    def genLabel(self, orderItem) :
        # カンバス作成
        label_path  = 'Labels/' + 'label2' + '.pdf'
        context = canvas.Canvas(label_path, landscape(self.page_size))

        # フォント登録
        pdfmetrics.registerFont(TTFont(self.font_family, self.font_path))

        # ラベル描画
        font_size = 20
        context.setFont(self.font_family, font_size)
        width, height = self.page_size # 90x29mm
        context.drawCentredString(width / 2,
                                  height / 2 - font_size * 0.4,
                                  'ラベル印刷サンプル2')
        context.showPage()

        # ファイル保存
        context.save()
