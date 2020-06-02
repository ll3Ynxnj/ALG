# Aikiki Label Generator
Ver.1.1
## 使用方法
入力用ディレクトリに指定された形式のtxtもしくはcsvを配置し、run.shを実行します。
### CSV形式での入力
ショップから取得したcsvファイルをそのまま入力用ディレクトリに配置します。
### テキスト形式での入力
各プラットフォームの形式に則したtxtファイルを入力用ディレクトリに配置します。ショップからのCSVに含まれない注文の入力に使用します。以下に各形式の説明を記します。
#### Minne用の形式
ヘッダは二行です。一行目は「-ORDER-M」、二行目は空にする必要があります。
データは七行です。上から氏名、郵便番号、住所、電話番号、商品コード、メモ欄です。七行目は空にする必要があります。
商品コードは商品ごとに「/」で区切ります。種別とオプションは「 」で区切ります。大文字、小文字は問いません。
以下に例を示します。
```
-ORDER-M

安伊 紀樹 M
〒105-0011
東京都港区芝公園４丁目2-8
03-1234-5678
hd b w / ps n
メモ欄、一人目のお客様

阿井 来岐 M
〒556-0002
大阪府大阪市浪速区恵美須東１丁目18−6
06-6012-3456
ps s / ps s n
メモ欄、二人目のお客様

```
#### Creema用の形式
ヘッダは二行です。一行目は「-ORDER-C」、二行目は空にする必要があります。
データは五行です。上から郵便番号と住所、氏名、商品コード、メモ欄です。五行目は空にする必要があります。
商品コードは商品ごとに「/」で区切ります。種別とオプションは「 」で区切ります。大文字、小文字は問いません。
以下に例を示します。
```
-ORDER-C

1050011東京都港区芝公園４丁目2-8(Japan)
安伊 紀樹 C
hd b w / ps n
メモ欄、一人目のお客様

5560002大阪府大阪市浪速区恵美須東１丁目18-6(Japan)
阿井 来岐 C
ps s / ps s n
メモ欄、二人目のお客様

```
#### 印刷用の形式
ヘッダは二行です。一行目は「-LABEL」、二行目は空にする必要があります。
データは八行です。上から宛先一行目、宛先二行目、宛名、商品コード、差出人、印刷の数量、メモ欄として使われることを想定していますが、ラベル印刷用の形式であり、注文処理を通さないため、各行に任意の文字列を入力可能です。ただし、六行目は整数値、八行目は空にする必要があります。
以下に例を示します。
```
-LABEL

〒227-0038 神奈川県横浜市（宛先一行目）
青葉区奈良3-14-1-8-908（宛先二行目）
川合 智香子（宛名）
（商品コード欄ですがなんでも入力可）
Aikiki 神奈川県横浜市青葉区奈良3-14-1-8-908（差出人欄ですがなんでも入力可）
3
上の行は数量です。整数値のみ入力可。ここはメモ欄です。ラベルには印刷されません。

〒227-0038 神奈川県横浜市（宛先一行目欄ですがなんでも入力可）
青葉区奈良3-14-1-8-908（宛先二行目欄ですがなんでも入力可）
川合 智香子（宛名欄ですがなんでも入力可）
（商品コード欄ですがなんでも入力可）
Aikiki 神奈川県横浜市青葉区奈良3-14-1-8-908（差出人欄ですがなんでも入力可）
1
上の行は数量です。整数値のみ入力可。ここはメモ欄です。ラベルには印刷されません。
```