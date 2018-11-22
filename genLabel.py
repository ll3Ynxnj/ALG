# coding:utf-8

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

import webbrowser

# 源真ゴシック（ http://jikasei.me/font/genshin/）
GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"

# 白紙をつくる（90x29mm）
FILENAME = 'label.pdf'
PAGESIZE = (90*mm,29*mm)
context = canvas.Canvas(FILENAME, pagesize=landscape(PAGESIZE))

# フォント登録
pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
font_size = 20
context.setFont('GenShinGothic', font_size)

# 真ん中に文字列描画
width, height = PAGESIZE # 90x29mm
context.drawCentredString(width / 2, height / 2 - font_size * 0.4, 'ラベル印刷サンプル')

# Canvasに書き込み
context.showPage()
# ファイル保存
context.save()

# ブラウザーで表示
webbrowser.open(FILENAME)
